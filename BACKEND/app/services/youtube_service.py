from __future__ import annotations

from typing import Any

import httpx

from app.core.config import get_settings


YOUTUBE_SEARCH_URL = (
    "https://www.googleapis.com/youtube/v3/search"
)


class YouTubeService:
    """Read-only YouTube search service for learning resources."""

    def __init__(self) -> None:
        self.settings = get_settings()

        if not self.settings.youtube_api_key:
            raise RuntimeError(
                "YOUTUBE_API_KEY is not configured."
            )

    def search_videos(
        self,
        query: str,
        *,
        max_results: int = 5,
    ) -> list[dict[str, Any]]:

        params = {
            "part": "snippet",
            "q": query,
            "key": self.settings.youtube_api_key,
            "type": "video",
            "maxResults": min(max_results, 10),
            "videoCaption": "closedCaption",
            "videoEmbeddable": "true",
            "safeSearch": "strict",
            "relevanceLanguage": "en",
            "regionCode": "IN",
            "order": "relevance",
        }

        with httpx.Client(timeout=15.0) as client:

            response = client.get(
                YOUTUBE_SEARCH_URL,
                params=params,
            )

            response.raise_for_status()

            data = response.json()

        results: list[dict[str, Any]] = []

        for item in data.get("items", []):

            video_id = (
                item.get("id", {})
                .get("videoId")
            )

            snippet = item.get(
                "snippet",
                {},
            )

            if not video_id:
                continue

            results.append(
                {
                    "video_id": video_id,
                    "title": snippet.get(
                        "title",
                        "",
                    ),
                    "description": snippet.get(
                        "description",
                        "",
                    ),
                    "channel_title": snippet.get(
                        "channelTitle",
                        "",
                    ),
                    "published_at": snippet.get(
                        "publishedAt",
                    ),
                    "thumbnail_url": (
                        snippet
                        .get("thumbnails", {})
                        .get("high", {})
                        .get("url")
                    ),
                    "url": (
                        f"https://www.youtube.com/watch?v="
                        f"{video_id}"
                    ),
                }
            )

        return results