# WareHouseCC 
## An Entity Extraction API driven by Whisper and Flask
<br>

## WareHouseCC or WareHouseChatClient is an LLM Based Specific Entity Extraction Technique for extracting Data from Messages for Warehouse Transactions.
<img width="2048" alt="Screenshot 2024-09-14 at 14 26 22" src="https://github.com/user-attachments/assets/ee79fb2b-f0da-48a0-a3da-4bf70140ed96">

### This project implements an API for extracting entities from both text and audio inputs. It uses a local model served via an API (like Ollama) for entity extraction and Whisper for transcribing audio files into text.

<br>

## Features

- Extract entities such as `processType`, `transactionType`, `itemName`, `locationFrom`, and `locationTo` from text-based user inputs.
- Transcribe audio files using OpenAI's Whisper model and extract entities from the transcribed text.

<br> 

## Prerequisites

Ensure you have the following installed before setting up the project:

- **Python 3.8+**
- **Pip** for installing Python packages
- **Whisper** for audio transcription
- **Flask** for running the web server
- **Ollama** (or any other local OpenAI-style API running on `localhost:11434`)

<br>

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/SetuBaru/WareHouseCC.git)
   cd WareHouseCC
   pip install -r requirements.txt
   python app.py
   ```
   
### This should run the flask web app on the following server "http://127.0.0.1:5000"
   
2. **To Call this API**
<img width="783" alt="Screenshot 2024-09-21 at 17 37 16" src="https://github.com/user-attachments/assets/3ae49474-39db-4346-af0a-45f6bbc96d7e">

For Text Input

   ```bash
     curl -X POST http://127.0.0.1:5000/process-input \
    -H "Content-Type: application/json" \
    -d '{"text": "textual query"}'
   ```

   <br><br>
   
<img width="784" alt="Screenshot 2024-09-21 at 17 35 30" src="https://github.com/user-attachments/assets/820faa8b-bd6f-4e6a-9cc5-69c7097fb81b">
     
  For Audio Input
     
      ```bash
    curl -X POST http://127.0.0.1:5000/process-audio \
    -H "Content-Type: multipart/form-data" \
    -F "audio=@/path/to/your/audio/file.mp3"```

<br><br>

   # Thank you
