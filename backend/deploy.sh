echo "🚀 Deploying SettleIn Backend to Google Cloud..."

# Variables
PROJECT_ID="maplepath"
REGION="us-central1"
SERVICE_NAME="maplepath-api"

# Set project
gcloud config set project $PROJECT_ID

# Enable services
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  sqladmin.googleapis.com \
  storage.googleapis.com \
  vision.googleapis.com

# Create Cloud SQL instance (if not exists)
gcloud sql instances create maplepath-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=$REGION

# Create database
gcloud sql databases create maplepath \
  --instance=maplepath-db

# Build and deploy
gcloud builds submit --config cloudbuild.yaml

echo "✅ Backend deployed successfully!"
echo "API URL: https://maplepath-api-xxxxx-uc.a.run.app"