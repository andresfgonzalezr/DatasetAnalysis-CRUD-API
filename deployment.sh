export GCP_PROJECT=nodal-bison-429004-b7
export SERVICE_NAME=api

gcloud config set project $GCP_PROJECT
# Compile the image and submit it to google cloud gcr
gcloud builds submit --tag=gcr.io/"${GCP_PROJECT}"/"${SERVICE_NAME}"
# Run previous docker image saved into cloud run
gcloud run deploy "${SERVICE_NAME}" --image=gcr.io/"${GCP_PROJECT}"/"${SERVICE_NAME}" --platform=managed --allow-unauthenticated