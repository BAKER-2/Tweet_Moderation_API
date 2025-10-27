# Tweet Moderation API

A machine learning system for automatic tweet moderation.  
The model identifies whether a tweet contains foul or abusive language and classifies it into specific subtypes such as toxic, obscene, or threatening.  
The system includes a web-based user interface, REST API endpoints, and full deployment on Google Cloud Run.

## 1. Live Demo

**Web Application:**  
https://tweet-moderation-799715076737.europe-west1.run.app  

**API Documentation (Swagger):**  
https://tweet-moderation-799715076737.europe-west1.run.app/docs  

**Health Check:**  
https://tweet-moderation-799715076737.europe-west1.run.app/health  

## 2. Overview

This project performs tweet classification and moderation using natural language processing (NLP).  
It combines a TF–IDF text vectorizer with a Logistic Regression model to predict:
- Binary foul/clean labels.
- Multi-label foulness subtypes.
- A 0–10 foulness severity score based on detected subtypes.

All predictions are exposed through a REST API built with FastAPI.  
A simple front-end interface allows interactive testing directly in the browser.

## 3. Architecture
      ┌──────────────────────┐
      │   User Input (UI)    │
      └──────────┬───────────┘
                 │
                 ▼
      ┌──────────────────────┐
      │   FastAPI Backend    │
      │ - /predict endpoint  │
      │ - /health, /docs     │
      └──────────┬───────────┘
                 │
                 ▼
      ┌──────────────────────┐
      │   ML Pipeline        │
      │ - TF-IDF Vectorizer  │
      │ - Logistic Regression│
      │ - Subtype Models     │
      └──────────┬───────────┘
                 │
                 ▼
      ┌──────────────────────┐
      │   JSON Response + UI │
      └──────────────────────┘

## 4. Tech Stack

| Layer | Technology |
|-------|-------------|
| Programming Language | Python 3.12 |
| ML Framework | scikit-learn |
| Vectorization | TF–IDF |
| Web Framework | FastAPI + Uvicorn |
| Deployment | Docker + Google Cloud Run |
| Frontend | HTML / CSS / JavaScript |

## 5. Model Summary

| Metric | Validation | Test |
|--------|-------------|------|
| Accuracy | 0.955 | 0.942 |
| F1 (macro) | 0.855 | 0.857 |
| ROC–AUC | 0.970 | 0.969 |
| Model | Logistic Regression |
| Threshold | 0.15 (optimized for recall) |

**Subtype classifiers:**  
toxic, severe_toxic, obscene, threat, insult, identity_hate  

Foulness Meter: computed on a 0–10 scale based on number and severity of active subtypes.

## 6. Running Locally

### 6.1 Clone and install

git clone https://github.com/BAKER-2/Tweet_Moderation_API.git
cd Tweet_Moderation_API
pip install -r requirements.txt

### 6.2 Run Locally 
uvicorn app.main:app --reload --port 8000
Then open:
	•	http://127.0.0.1:8000 → UI
	•	http://127.0.0.1:8000/docs → Swagger

## 7. Deployment (Google Cloud Run)

The service is containerized using Docker and deployed to Cloud Run.
Build and deploy steps:

REGION=europe-west1
PROJECT_ID=keen-genius-476408-c7
REPO_NAME=tweet-api-repo
IMAGE=$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/tweet-moderation:latest

gcloud builds submit --tag $IMAGE
gcloud run deploy tweet-moderation \
  --image $IMAGE \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --memory 1Gi

## 8. Repository Structure

app/
 ├── main.py               → FastAPI application
 ├── models/               → Pickled ML models
 ├── tests                 
 
requirements.txt
Dockerfile
README.md

## 9. Authors
Baker huseyin - 1901345
Islah Haoues - 1800272

## 10. License

This project is intended for academic and educational use within the scope of the NLP course assignment.
