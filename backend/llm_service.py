"""
LLM service — sends extracted label text + patient context to Groq
and returns structured drug interaction advice.
"""
import logging

import requests

from config import config

logger = logging.getLogger(__name__)


class LLMError(Exception):
    """Raised when the LLM cannot produce a usable response."""


def get_advice(label_text: str, age: int, conditions: str) -> str:
    """Send label text + patient context to Groq, return advice text."""
    if not config.has_ai_key():
        raise LLMError("GROQ_API_KEY is not set in .env")

    prompt = (
        "You are a medical safety assistant. Based on the following medicine "
        "label text and patient info, list any drug interaction warnings, "
        "dosage cautions, or conditions to watch for. Be concise and clear.\n\n"
        f"Label text:\n{label_text}\n\n"
        f"Patient age: {age}\n"
        f"Patient conditions: {conditions}\n"
    )

    payload = {
        "model": config.GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {"Authorization": f"Bearer {config.GROQ_API_KEY}"}

    try:
        response = requests.post(
            config.GROQ_URL, json=payload, headers=headers, timeout=20
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.RequestException as exc:
        logger.warning("Groq request failed: %s", exc)
        raise LLMError(f"Could not get advice from Groq: {exc}") from exc
    except (KeyError, IndexError) as exc:
        logger.warning("Unexpected Groq response format: %s", exc)
        raise LLMError("Groq returned an unexpected response format") from exc



