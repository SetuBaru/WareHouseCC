from flask import Flask, request, jsonify
from entity_extraction_api import ExtractEntity  # Adjust the import according to your file structure

app = Flask(__name__)


@app.route('/process-input', methods=['POST'])
def process_input():
    # Get JSON data from request
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    text_input = data['text']

    try:
        # Call the ExtractEntity function
        result = ExtractEntity(text_input)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
