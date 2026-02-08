"""Configuration management for Jared's Videos."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    """Application configuration loaded from environment variables."""

    google_cloud_project: str
    google_cloud_location: str
    google_genai_use_vertexai: bool = True

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        project = os.getenv("GOOGLE_CLOUD_PROJECT")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

        if not project:
            missing = [v for v in ["GOOGLE_CLOUD_PROJECT"] if not os.getenv(v)]
            raise ValueError(f"Missing required environment variables: {missing}")

        return cls(
            google_cloud_project=project,
            google_cloud_location=location,
            google_genai_use_vertexai=True,
        )

    def to_env_dict(self) -> dict[str, str]:
        """Convert config to environment variables dict for google-genai."""
        return {
            "GOOGLE_CLOUD_PROJECT": self.google_cloud_project,
            "GOOGLE_CLOUD_LOCATION": self.google_cloud_location,
            "GOOGLE_GENAI_USE_VERTEXAI": "true" if self.google_genai_use_vertexai else "false",
        }


def load_config() -> Config:
    """Load and validate configuration."""
    return Config.from_env()
