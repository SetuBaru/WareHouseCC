from flask import Flask, request, jsonify
from entity_extraction_api import ExtractEntity
import whisper
import os

app = Flask(__name__)

# Load the Whisper model (you can choose different models: tiny, base, small, medium, large)
model = whisper.load_model("base")

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


@app.route('/process-audio', methods=['POST'])
def process_audio():
    # Ensure an audio file is provided
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']

    # Save the audio file temporarily
    audio_path = os.path.join("temp_audio", audio_file.filename)
    audio_file.save(audio_path)

    try:
        # Transcribe the audio using Whisper
        transcription = model.transcribe(audio_path)
        text_input = transcription['text']

        # Call the ExtractEntity function with the transcribed text
        result = ExtractEntity(text_input)

        # Clean up the temporary audio file
        os.remove(audio_path)

        return jsonify({
            "transcription": text_input,
            "extracted_entities": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Ensure the temp_audio directory exists
    if not os.path.exists("temp_audio"):
        os.makedirs("temp_audio")

    app.run(debug=True)
