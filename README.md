# YouTube Transcript API

This project is a simple Flask server that provides API endpoints for retrieving pure-text transcripts for YouTube videos. It also provides the ability to translate transcripts into different languages.

## API Endpoints

### POST /api/transcript

**Request:**

- `video_url` (string): The URL of the YouTube video.
- `language` (string): The language code for translation (default is 'en').

**Response:**

- `transcript` (string): The translated or original transcript text.

**Example Request:**

```bash
curl -X POST https://your-vercel-url/api/transcript \
-H "Content-Type: application/json" \
-d '{
  "video_url": "YOUR_YOUTUBE_VIDEO_URL",
  "language": "en"
}'
