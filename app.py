from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


def send_to_fmp(payload):
    """
    Placeholder for your FileMaker Data API call.
    Replace this with your FMP integration logic.
    """
    logging.info("Sending payload to FMP:")
    logging.info(payload)
    # simulate response
    return {"success": True, "processed": len(payload.get("shots", []))}


@app.route("/post", methods=["POST"])
def shotgrid_ami():
    # Normalize incoming data to a standard dict
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()  # handles application/x-www-form-urlencoded

    logging.info("Received ShotGrid request:")
    logging.info(data)

    # Extract expected args
    entity_id = data.get("entity_id")
    entity_type = data.get("entity_type")
    project_id = data.get("project_id")
    user_id = data.get("user_id")

    # Validate required args
    if not all([entity_id, entity_type, project_id, user_id]):
        return jsonify({
            "status": "error",
            "message": "Missing required ShotGrid args",
            "received": data
        }), 400

    # Build standardized payload for FMP
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

    # Send to FMP or other processing function
    fmp_response = send_to_fmp(payload)

    return jsonify({
        "status": "ok",
        "fmp_response": fmp_response
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
