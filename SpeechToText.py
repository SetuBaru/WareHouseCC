from flask import Flask, request, jsonify
import whisper

app = Flask(__name__)

# Load Whisper model
model = whisper.load_model("base")  # You can choose different models: tiny, base, small, medium, large

@app.route('/convert-audio', methods=['POST'])
def convert_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Save the file to a temporary location
        temp_file_path = "/tmp/temp_audio_file.wav"
        file.save(temp_file_path)
        
        # Transcribe the audio file using Whisper
        result = model.transcribe(temp_file_path)
        
        # Remove the temporary file
        os.remove(temp_file_path)
        
        # Return the transcribed text
        return jsonify({"text": result['text']})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
