# Jared's Videos

Video generation using Google Vertex AI Veo 3.

## Prerequisites

- Python 3.11+
- Google Cloud account with Vertex AI API enabled
- GCS bucket for storing generated videos
- Application Default Credentials (ADC) configured

## Setup

1. **Clone and install dependencies:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

2. **Configure Google Cloud authentication:**

   ```bash
   gcloud auth application-default login
   ```

3. **Set up environment variables:**

   ```bash
   cp .env.example .env
   # Edit .env with your Google Cloud project details
   ```

4. **Create a GCS bucket for video output:**

   ```bash
   gsutil mb gs://your-bucket-name
   ```

## Usage

```python
from jareds_videos import VideoGenerator, VideoGenerationRequest, load_config

config = load_config()
generator = VideoGenerator(config)

request = VideoGenerationRequest(
    prompt="A serene mountain landscape at sunset with clouds drifting by",
    output_gcs_uri="gs://your-bucket/videos/",
)

result = generator.generate(request)
print(f"Generated video: {result.video_uri}")
```

## Development

- **Format and lint:** `ruff check . && ruff format .`
- **Type check:** `mypy src/`
- **Run tests:** `pytest`

## Project Structure

```
jareds-videos/
├── src/jareds_videos/
│   ├── __init__.py         # Package exports
│   ├── config.py           # Configuration management
│   └── video_generator.py  # Veo video generation client
├── pyproject.toml          # Project metadata and dependencies
├── .env.example            # Environment variable template
└── README.md               # This file
```
