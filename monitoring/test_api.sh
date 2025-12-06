podman stop churn-api-container
podman rm churn-api-container
podman run -d --name churn-api-container -p 5000:5000 --network=host -v "$(pwd)/model:/app/model:Z" -v "./logs:/app/logs:Z" localhost/churn-api:latest

sleep 3

#Test with Curl
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d @input.json

