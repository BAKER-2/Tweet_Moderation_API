
# Tweet Moderation API

FastAPI app to classify tweets as foul or proper, with multi-label subtypes, tags, and a 0–10 foulness meter.

## Run locally
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

## Docker
docker build -t tweet-moderation .
docker run -p 8000:8000 tweet-moderation
