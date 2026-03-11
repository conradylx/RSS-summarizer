from openai import OpenAI
import logging
from app.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a text summarization tool. "
    "Your only job is to summarize the provided text in 3-4 sentences"
    "in the same language as the text. "
    "Never refuse, never ask questions, never add commentary. "
    "Just output the summary and nothing else."
)

client = OpenAI(
    base_url=settings.ollama_url,
    api_key="ollama",
    timeout=120.0,
)


def summarize(text: str) -> str:
    if not text:
        return ""

    try:
        response = client.chat.completions.create(
            model="llama3.2:1b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text[:1000]},
            ],
            max_tokens=150,
            temperature=0.3,
        )
        content = response.choices[0].message.content or ""
        logger.info("Summarized (%d chars)", len(content))
        return content
    except Exception as e:
        logger.error("Summarize error: %s", e)
        return ""
