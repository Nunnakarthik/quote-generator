# Daily Spark 🔥 — Quote Generator

A space-themed quote generator built with Flask, featuring live quotes from the ZenQuotes API with offline fallback support, an animated night-sky UI, and a fully automated CI/CD pipeline.

**Live demo:** https://quotegenerator-rho-lake.vercel.app

![CI/CD Pipeline](https://github.com/Nunnakarthik/quote-generator/actions/workflows/ci-cd.yml/badge.svg)

---

## ✨ Features

- **Live quotes** pulled from the [ZenQuotes API](https://zenquotes.io), with a curated 80+ quote local fallback library for offline/resilient use
- **Animated space theme** — twinkling stars, a slow-drifting satellite, and occasional shooting stars, all rendered on HTML canvas
- **Text-to-stars transition** — clicking "New quote" dissolves the current quote into glowing star particles, then reassembles the new quote from stars
- **Copy & Share** buttons for quick sharing
- Fully responsive design

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Frontend:** Vanilla JS, HTML5 Canvas, CSS animations
- **Testing:** pytest, pytest-cov
- **Containerization:** Docker
- **CI/CD:** GitHub Actions (lint → test → build → security scan)
- **Security:** Trivy vulnerability scanning on the Docker image
- **Deployment:** Vercel

## 📦 Project Structure

```
├── app.py                      # Flask app (routes, quote logic, HTML template)
├── test_app.py                 # pytest test suite
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container build instructions
├── .dockerignore
├── vercel.json                 # Vercel routing config
└── .github/
    └── workflows/
        └── ci-cd.yml           # CI/CD pipeline definition
```

## 🚀 Running Locally

**Prerequisites:** Python 3.11+, Docker Desktop (optional, for containerized run)

```bash
# Clone the repo
git clone https://github.com/Nunnakarthik/quote-generator.git
cd quote-generator

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.
Visit https://quotegenerator-rho-lake.vercel.app in your browser.

### Run with Docker

```bash
docker build -t quote-generator .
docker run -p 5000:5000 quote-generator
```

### Run tests

```bash
pytest --cov=app --cov-report=term-missing
```

## 🔄 CI/CD Pipeline

Every push to `main` automatically triggers a 4-stage GitHub Actions pipeline:

1. **Lint** — checks code style with flake8
2. **Test** — runs the pytest suite with coverage reporting
3. **Build** — builds the Docker image
4. **Security scan** — scans the built image for vulnerabilities using Trivy

See the [Actions tab](https://github.com/Nunnakarthik/quote-generator/actions) for live pipeline runs.

## 📡 API Endpoints

| Route | Description |
|---|---|
| `GET /` | Homepage — renders a quote instantly, then upgrades to a live one |
| `GET /quote` | Returns a random quote (JSON) |
| `GET /quote/today` | Returns the quote of the day (JSON) |

## 📝 License

This project is for educational purposes as part of a CI/CD pipeline learning exercise.