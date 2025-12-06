from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from PIL import Image
import requests
import os
import base64
import io
import time

# -------------------------
# Flask setup
# -------------------------
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
app.secret_key = "super-secret-key"

# -------------------------
# Dummy in-memory user store
# -------------------------
USERS = {}

# -------------------------
# OpenRouter config
# -------------------------
OPENROUTER_API_KEY = "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"  # 🔑 Replace
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_PARALYSIS = "meta-llama/llama-3.1-8b-instruct"
MODEL_CHATBOT = "meta-llama/llama-3.1-8b-instruct"

# -------------------------
# Helper: OpenRouter call
# -------------------------
def call_openrouter(prompt, model=MODEL_CHATBOT, retries=2, timeout=30):
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": (
                "You are a medical assistant specialized in detecting facial and speech paralysis."
            )},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 400,
        "temperature": 0.5
    }
    for _ in range(retries):
        try:
            r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=timeout)
            if r.status_code == 200:
                data = r.json()
                return data["choices"][0]["message"]["content"].strip()
            print("Error:", r.text)
        except Exception as e:
            print("Request error:", e)
            time.sleep(1)
    return ""

# -------------------------
# Image compressor
# -------------------------
def prepare_image_snippet(file_stream, max_size=512, quality=65, snippet_len=3500):
    try:
        img = Image.open(file_stream).convert("RGB")
        w, h = img.size
        if max(w, h) > max_size:
            ratio = max_size / float(max(w, h))
            img = img.resize((int(w * ratio), int(h * ratio)))
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality)
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        return {"snippet": b64[:snippet_len], "width": img.width, "height": img.height}
    except Exception as e:
        print("Image error:", e)
        return None

# -------------------------
# AUTH ROUTES
# -------------------------
@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in USERS:
            flash("Username already exists!", "danger")
            return redirect(url_for("register"))
        USERS[username] = password
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if USERS.get(username) == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        flash("Invalid credentials!", "danger")
        return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully!", "info")
    return redirect(url_for("landing"))

# -------------------------
# DASHBOARD
# -------------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("Please log in to continue.", "warning")
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])

# -------------------------
# UPLOAD IMAGE PAGE + AI
# -------------------------
@app.route("/upload_page")
def upload_page():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return "No file uploaded", 400
    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)
    file.seek(0)
    snippet = prepare_image_snippet(file)
    if not snippet:
        return render_template("result.html", image_path=path, result="Image processing failed.", confidence="N/A")
    prompt = (
        "Analyze the following face image for paralysis signs. "
        f"Metadata: width={snippet['width']}, height={snippet['height']}. "
        f"BASE64_SNIPPET: {snippet['snippet']}"
    )
    result = call_openrouter(prompt, MODEL_PARALYSIS)
    if not result:
        result = "⚠️ AI could not analyze the image. Try again."
    return render_template("result.html", image_path=path, result=result, confidence="AI Estimated")

# -------------------------
# UPLOAD VOICE PAGE + AI
# -------------------------
@app.route("/upload_voice_page")
def upload_voice_page():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("upload_voice.html")

@app.route("/upload_voice", methods=["POST"])
def upload_voice():
    file = request.files.get("voice")
    if not file:
        return "No voice file uploaded!", 400
    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)
    file.seek(0)
    b64 = base64.b64encode(file.read()).decode("utf-8")[:3500]
    prompt = (
        "Analyze this voice for slurred or impaired speech possibly due to paralysis. "
        f"AUDIO_SNIPPET: {b64}"
    )
    result = call_openrouter(prompt, MODEL_PARALYSIS)
    if not result:
        result = "⚠️ AI could not analyze the voice."
    return render_template("result.html", image_path=None, result=result, confidence="AI Estimated")

# -------------------------
# CHATBOT
# -------------------------
@app.route("/chatbot")
def chatbot():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("chatbot.html")

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "").strip()
    if not msg:
        return jsonify({"reply": "Please enter a question."})
    allowed = ["paralysis", "facial", "speech", "stroke", "therapy", "recovery"]
    if not any(w in msg.lower() for w in allowed):
        return jsonify({"reply": "I only answer medical questions about paralysis or speech issues."})
    reply = call_openrouter(msg, MODEL_CHATBOT)
    return jsonify({"reply": reply or "⚠️ AI did not respond."})

# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
