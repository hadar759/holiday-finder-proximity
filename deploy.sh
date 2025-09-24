#!/bin/bash

# Deploy Holiday Finder API to Google Cloud Run
gcloud run deploy holiday-finder-proximity-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 3 \
  --min-instances 0