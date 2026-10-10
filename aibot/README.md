# Druva R - AI Candidate Interview Assistant 🤖

An interactive, AI-driven candidate representation portal powered by FastAPI, Groq (GPT-OSS-120B / LLaMA), and a modern glassmorphic web UI.

---

## 🚀 Live Deployment on Render (Free Tier)

### Step 1: Push code to GitHub
```bash
git add aibot/
git commit -m "Add AI candidate interview portal"
git push origin main
```

### Step 2: Create a Free Web Service on Render
1. Go to [Render Dashboard](https://dashboard.render.com/) and click **New +** -> **Web Service**.
2. Connect your GitHub repository (`genai-journey`).
3. Configure the following fields:
   - **Name**: `druva-ai-interview`
   - **Region**: Closest to you (e.g., Singapore / Frankfurt / Oregon)
   - **Root Directory**: `aibot`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.chatBot:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`
4. Under **Environment Variables**, add:
   - `GROQ_API_KEY`: *Your Groq API key*
5. Click **Deploy Web Service**!

Render will build and deploy your app. Once deployed, you get a free live URL:
`https://druva-ai-interview.onrender.com`

---

## 💻 Local Development

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run FastAPI Application
```bash
uvicorn backend.chatBot:app --reload
```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.
