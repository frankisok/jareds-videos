"""Video generation client using Google Vertex AI Veo 3."""

import os
from dataclasses import dataclass

from google import genai
from google.genai.types import GenerateVideosConfig

from jareds_videos.config import Config


@dataclass
class VideoGenerationRequest:
    """Request parameters for video generation."""

    prompt: str
    output_gcs_uri: str
    model: str = "veo-2.0-generate-001"  # Default Veo model
    negative_prompt: str | None = None
    aspect_ratio: str = "16:9"
    duration_seconds: int = 8
    person_generation: str = "allow_adult"
    seed: int | None = None
    enhance_prompt: bool = False
    generate_audio: bool = True
    enable_prompt_rewriting: bool = False


@dataclass
class VideoGenerationResult:
    """Result of a video generation operation."""

    video_uri: str
    operation_id: str
    status: str


class VideoGenerator:
    """Client for generating videos using Vertex AI Veo."""

    def __init__(self, config: Config) -> None:
        """Initialize the video generator with configuration."""
        self._config = config
        self._client: genai.Client | None = None

    @property
    def client(self) -> genai.Client:
        """Get or create the genai client."""
        if self._client is None:
            # Set environment variables for google-genai
            for key, value in self._config.to_env_dict().items():
                os.environ[key] = value

            self._client = genai.Client()
        return self._client

    def generate(self, request: VideoGenerationRequest) -> VideoGenerationResult:
        """Generate a video based on the prompt.

        Args:
            request: The video generation request parameters.

        Returns:
            VideoGenerationResult containing the video URI and operation details.
        """
        config = GenerateVideosConfig(
            aspect_ratio=request.aspect_ratio,
            output_gcs_uri=request.output_gcs_uri,
            person_generation=request.person_generation,
            negative_prompt=request.negative_prompt,
            duration_seconds=request.duration_seconds,
            seed=request.seed,
            enhance_prompt=request.enhance_prompt,
            generate_audio=request.generate_audio,
            enable_prompt_rewriting=request.enable_prompt_rewriting,
        )

        operation = self.client.models.generate_videos(
            model=request.model,
            prompt=request.prompt,
            config=config,
        )

        # Wait for the operation to complete
        operation.wait()

        if operation.result and operation.result.generated_videos:
            video = operation.result.generated_videos[0]
            return VideoGenerationResult(
                video_uri=video.video.uri,
                operation_id=operation.name,
                status="completed",
            )

        raise RuntimeError("Video generation failed: no video produced")

    async def generate_async(self, request: VideoGenerationRequest) -> VideoGenerationResult:
        """Generate a video asynchronously.

        Args:
            request: The video generation request parameters.

        Returns:
            VideoGenerationResult containing the video URI and operation details.
        """
        config = GenerateVideosConfig(
            aspect_ratio=request.aspect_ratio,
            output_gcs_uri=request.output_gcs_uri,
            person_generation=request.person_generation,
            negative_prompt=request.negative_prompt,
            duration_seconds=request.duration_seconds,
            seed=request.seed,
            enhance_prompt=request.enhance_prompt,
            generate_audio=request.generate_audio,
            enable_prompt_rewriting=request.enable_prompt_rewriting,
        )

        operation = await self.client.aio.models.generate_videos(
            model=request.model,
            prompt=request.prompt,
            config=config,
        )

        await operation.wait()

        if operation.result and operation.result.generated_videos:
            video = operation.result.generated_videos[0]
            return VideoGenerationResult(
                video_uri=video.video.uri,
                operation_id=operation.name,
                status="completed",
            )

        raise RuntimeError("Video generation failed: no video produced")
