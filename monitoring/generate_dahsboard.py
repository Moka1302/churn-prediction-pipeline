# Install matplotlib if you haven't
pip install matplotlib

# Make some predictions (at least 10)

for i in {1..2}; do
  curl -X POST http://localhost:5000/predict \
    -H "Content-Type: application/json" \
    -d @input.json
  sleep 1
done

# Create dashboard
python view_dashboard.py

# Dashboard saved to logs/dashboard.png
