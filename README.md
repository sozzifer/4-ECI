gcloud builds submit --tag gcr.io/stat4002/confidence-intervals  --project=stat4002

gcloud run deploy --image gcr.io/stat4002/confidence-intervals --platform managed  --project=stat4002 --allow-unauthenticated