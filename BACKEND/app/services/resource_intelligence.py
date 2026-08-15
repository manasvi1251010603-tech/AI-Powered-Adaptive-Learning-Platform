from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from openai import OpenAI
from youtube_transcript_api import (
    YouTubeTranscriptApi,
)

from app.core.config import get_settings


@dataclass
class TranscriptChunk:
    start_seconds: float
    end_seconds: float
    text: str


@dataclass
class RecommendedSection:
    start_seconds: float
    end_seconds: float
    concept: str
    reason: str
    confidence: float


class ResourceIntelligenceService:
    """Find and map external learning resources to concepts."""

    def __init__(self) -> None:

        settings = get_settings()

        if not settings.openai_api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured."
            )

        self.client = OpenAI(
            api_key=settings.openai_api_key
        )

        self.model = settings.openai_model_general

    # --------------------------------------------------------
    # TRANSCRIPT
    # --------------------------------------------------------

    def get_transcript(
        self,
        video_id: str,
    ) -> list[TranscriptChunk]:

        transcript_api = YouTubeTranscriptApi()

        transcript = transcript_api.fetch(
            video_id
        )

        chunks: list[TranscriptChunk] = []

        for item in transcript:

            start = float(item.start)

            duration = float(
                item.duration
            )

            end = start + duration

            text = item.text.strip()

            if not text:
                continue

            chunks.append(
                TranscriptChunk(
                    start_seconds=start,
                    end_seconds=end,
                    text=text,
                )
            )

        return chunks

    # --------------------------------------------------------
    # COMBINE SMALL TRANSCRIPT ENTRIES
    # --------------------------------------------------------

    def combine_transcript_chunks(
        self,
        chunks: list[TranscriptChunk],
        *,
        window_seconds: float = 30.0,
    ) -> list[TranscriptChunk]:

        if not chunks:
            return []

        combined: list[TranscriptChunk] = []

        current_start = chunks[0].start_seconds
        current_end = chunks[0].end_seconds
        current_text = [chunks[0].text]

        for chunk in chunks[1:]:

            if (
                chunk.end_seconds
                - current_start
                <= window_seconds
            ):
                current_end = chunk.end_seconds
                current_text.append(chunk.text)

            else:

                combined.append(
                    TranscriptChunk(
                        start_seconds=current_start,
                        end_seconds=current_end,
                        text=" ".join(
                            current_text
                        ),
                    )
                )

                current_start = (
                    chunk.start_seconds
                )
                current_end = (
                    chunk.end_seconds
                )
                current_text = [chunk.text]

        combined.append(
            TranscriptChunk(
                start_seconds=current_start,
                end_seconds=current_end,
                text=" ".join(
                    current_text
                ),
            )
        )

        return combined

    # --------------------------------------------------------
    # AI CONCEPT → TIMESTAMP MAPPING
    # --------------------------------------------------------

    def map_concept_to_transcript(
        self,
        *,
        concept_name: str,
        concept_description: str,
        transcript: list[TranscriptChunk],
        mastery_score: float,
    ) -> list[RecommendedSection]:

        if not transcript:
            return []

        transcript_text = "\n".join(
            (
                f"[{chunk.start_seconds:.1f}-"
                f"{chunk.end_seconds:.1f}] "
                f"{chunk.text}"
            )
            for chunk in transcript
        )

        prompt = f"""
You are the resource-matching engine for an
adaptive learning platform.

Learner concept:
{concept_name}

Concept description:
{concept_description}

Current learner mastery:
{mastery_score}/100

The learner needs help with this concept.

Below is a timestamped transcript from an existing
educational video.

TRANSCRIPT:
{transcript_text}

Your task:

1. Find transcript ranges that genuinely teach
   the requested concept.
2. Ignore introductions, advertisements, unrelated
   material and advanced material unless it directly
   teaches the concept.
3. Prefer the smallest useful contiguous ranges.
4. Do not invent timestamps.
5. Every timestamp must correspond to the transcript.
6. Return at most 3 useful sections.
7. If the transcript does not adequately teach the
   concept, return an empty list.

Return ONLY valid JSON:

{{
  "sections": [
    {{
      "start_seconds": 0,
      "end_seconds": 0,
      "concept": "string",
      "reason": "string",
      "confidence": 0.0
    }}
  ]
}}
"""

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        raw_output = response.output_text.strip()

        try:
            parsed = json.loads(
                raw_output
            )

        except json.JSONDecodeError:
            return []

        sections = parsed.get(
            "sections",
            [],
        )

        results: list[
            RecommendedSection
        ] = []

        transcript_start = min(
            chunk.start_seconds
            for chunk in transcript
        )

        transcript_end = max(
            chunk.end_seconds
            for chunk in transcript
        )

        for section in sections:

            try:
                start = float(
                    section["start_seconds"]
                )

                end = float(
                    section["end_seconds"]
                )

                confidence = float(
                    section.get(
                        "confidence",
                        0,
                    )
                )

            except (
                KeyError,
                TypeError,
                ValueError,
            ):
                continue

            # ------------------------------------------------
            # HARD VALIDATION
            # AI is not authoritative.
            # ------------------------------------------------

            if start < transcript_start:
                continue

            if end > transcript_end:
                continue

            if end <= start:
                continue

            if confidence < 0 or confidence > 1:
                continue

            results.append(
                RecommendedSection(
                    start_seconds=start,
                    end_seconds=end,
                    concept=str(
                        section.get(
                            "concept",
                            concept_name,
                        )
                    ),
                    reason=str(
                        section.get(
                            "reason",
                            "",
                        )
                    ),
                    confidence=confidence,
                )
            )

        return results