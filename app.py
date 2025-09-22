from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "ShotGrid → FileMakerPro API is running!"

@app.route("/process_shots", methods=["POST"])
def process_shots():
    data = request.json
    # Example: log the data to confirm receipt
    print("Received from SG:", data)
    
    # TODO: Call your FMP API logic here using the data
    # For now, just return a dummy response
    response = {"status": "success", "processed": len(data.get("selected_ids", []))}
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
