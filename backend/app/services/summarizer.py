from openai import OpenAI
import logging
from app.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "Summarize the following article in 2-3 sentences "
    "in the same language as the article."
)

client = OpenAI(
    base_url=settings.ollama_url,
    api_key="ollama",
    timeout=60.0,
)


def summarize(text: str) -> str:
    if not text:
        return ""

    try:
        response = client.chat.completions.create(
            model="llama3.2",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text[:2000]},
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
