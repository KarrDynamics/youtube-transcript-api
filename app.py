from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route('/api/transcript', methods=['POST'])
def get_transcript():
    data = request.json
    video_url = data.get('video_url')
    language = data.get('language', 'en')

    # Extract video ID from the URL
    video_id = video_url.split('v=')[-1]

    try:
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
        return jsonify({'error': 'Transcripts are disabled for this video.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
