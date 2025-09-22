# app.py
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(level=logging.INFO)

# -----------------------------
# Dummy FMP integration
# -----------------------------
def send_to_fmp(payload):
    """
    Placeholder function for sending data to FileMaker Data API.
    Replace with your API call logic.
    """
    logging.info("Preparing to send to FMP:")
    logging.info(payload)
    # Example: requests.post(fmp_url, json=payload, headers=headers)
    return {"status": "success", "sent_count": len(payload.get("shots", []))}

# -----------------------------
# AMI Endpoint
# -----------------------------
@app.route("/post", methods=["POST"])
def shotgrid_ami():
    # Get data from JSON body or form data
    data = request.json or request.form
    logging.info("Received ShotGrid request:")
    logging.info(data)

    # Extract expected args from ShotGrid
    args = data.get("args") or {}
    entity_id = args.get("entity_id")
    entity_type = args.get("entity_type")
    project_id = args.get("project_id")
    user_id = args.get("user_id")

    # Validate basic fields
    if not all([entity_id, entity_type, project_id, user_id]):
        return jsonify({"status": "error", "message": "Missing required ShotGrid args"}), 400

    # Build payload for FMP
    payload = {
        "shots": [
            {
                "entity_id": entity_id,
                "entity_type": entity_type,
                "project_id": project_id,
                "user_id": user_id
            }
        ]
    }

    # Call placeholder FMP function
    fmp_response = send_to_fmp(payload)

    return jsonify({"status": "ok", "fmp_response": fmp_response})

# -----------------------------
# Health check (optional)
# -----------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "alive"})

if __name__ == "__main__":
    # For local testing only; Render uses gunicorn in production
    app.run(host="0.0.0.0", port=5000, debug=True)
