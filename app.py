from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from googletrans import Translator
from flask_cors import CORS
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
translator = Translator()
CORS(app)

@app.route('/api/transcript', methods=['POST'])
def get_transcript():
    logging.info("Received a request at /api/transcript")
    try:
        # Log the received request data
        data = request.json
        logging.info(f"Received request data: {data}")

        # Validate the request data
        if not data or 'video_url' not in data or 'language' not in data:
            logging.error("Invalid request data")
            return jsonify({"error": "Invalid request data"}), 400

        video_url = data.get('video_url')
        language = data.get('language', 'en')

        # Extract video ID from the URL
        video_id = video_url.split('v=')[-1]

        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Combine transcript text
        transcript_text = " ".join([item['text'] for item in transcript])

        # Translate transcript if necessary
        if language != 'en':
            translated_text = translator.translate(transcript_text, dest=language).text
            return jsonify({'transcript': translated_text})

        return jsonify({'transcript': transcript_text})

    except TranscriptsDisabled:
        logging.error("Transcripts are disabled for this video.")
        return jsonify({'error': 'Transcripts are disabled for this video.'}), 400
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An internal error occurred.'}), 500

if __name__ == '__main__':
    app.run(debug=False)
