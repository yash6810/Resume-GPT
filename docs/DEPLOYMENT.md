# 🚀 ResumeGPT Cloud Deployment Guide

This guide walks you through deploying **ResumeGPT** live on the web so anyone can access it from their browser.

---

## 🌟 Method 1: Render.com (Recommended Free Cloud)

Render allows you to connect your GitHub repository and automatically deploys your app whenever you push new changes.

### Step-by-Step:
1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Add Docker and deployment configs"
   git push origin main
   ```

2. **Create a Free Account on Render**:
   - Go to [render.com](https://render.com) and sign in with your GitHub account.

3. **Deploy Web Service**:
   - Click **New +** &rarr; **Web Service**.
   - Select your `Resume-GPT` repository.
   - Set the runtime to **Docker** (it will automatically detect the `Dockerfile` and `render.yaml`).
   - Choose the **Free Instance Type**.
   - Click **Deploy Web Service**.

4. **Your Live URL**:
   - Render will build the container and provide your live public URL:  
     `https://resumegpt-xxxx.onrender.com`

---

## 🤗 Method 2: Hugging Face Spaces (Free 16GB RAM Tier)

Hugging Face Spaces provides **16GB of RAM for free**, making it ideal for PyTorch and Sentence-Transformers.

### Step-by-Step:
1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) and click **Create new Space**.
2. Set Space Name: `resumegpt`.
3. Select License: `MIT` or `Open Source`.
4. Select Space SDK: **Docker** &rarr; **Blank**.
5. Set Visibility: **Public**.
6. Push your repository to the Hugging Face Space Git remote:
   ```bash
   git remote add space https://huggingface.co/spaces/YOUR_USERNAME/resumegpt
   git push space main
   ```
7. Hugging Face will automatically build and host your app live!

---

## 🐳 Method 3: Run with Docker Locally

To run the complete containerized app locally without installing Python or dependencies manually:

```bash
docker compose up --build
```
Then open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🔒 Production Checklist
- [x] CORS configuration in `backend/app/main.py`
- [x] Static frontend single-page app served from root `/`
- [x] Health check endpoint active at `/health`
- [x] Dynamic port binding (`${PORT:-8000}`)
