from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from googletrans import Translator
from flask_cors import CORS
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
translator = Translator()

@app.route('/api/transcript', methods=['POST'])
def get_transcript():
    if request.method == 'GET':
        return jsonify({"message": "Please use POST to submit video_url and language."})

    if request.method == 'POST':
        logging.info("Received a request at /api/transcript")
        
        if request.content_type != 'application/json':
            logging.error("Unsupported Media Type: Content-Type must be 'application/json'")
            return jsonify({"error": "Unsupported Media Type: Content-Type must be 'application/json'"}), 415

        data = request.json
        logging.info(f"Received request data: {data}")

        # TODO: Validate the format of the video_url (ensure it's a valid YouTube URL)
        if not data or 'video_url' not in data or 'language' not in data:
            logging.error("Invalid request data")
            return jsonify({"error": "Invalid request data"}), 400

        video_url = data.get('video_url')
        language = data.get('language', 'en')

        # Extract video ID from the URL
        video_id = video_url.split('v=')[-1]

        try:
            # Fetch the transcript
            logging.info(f"Fetching transcript for video ID: {video_id}")
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            logging.info("Transcript fetched successfully")

            # TODO: Handle cases where the transcript is empty or not available in the requested language
            # Combine transcript text
            transcript_text = " ".join([item['text'] for item in transcript])

            # Translate transcript if necessary
            if language != 'en':
                logging.info(f"Translating transcript to: {language}")
                translated_text = translator.translate(transcript_text, dest=language).text
                return jsonify({'result': [{'text': translated_text}]})

            return jsonify({'result': [{'text': transcript_text}]})

        except TranscriptsDisabled:
            logging.error("Transcripts are disabled for this video.")
            return jsonify({'error': 'Transcripts are disabled for this video.'}), 400
        except Exception as e:
            # TODO: Implement more specific error handling (e.g., handling network errors separately)
            logging.error(f"An error occurred: {str(e)}")
            return jsonify({'error': 'An internal error occurred.'}), 500

if __name__ == '__main__':
    app.run(debug=False)
