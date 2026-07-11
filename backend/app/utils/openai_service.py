from openai import OpenAI
from app.config import settings
import logging

logger = logging.getLogger(__name__)

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def summarize_notice(title: str, content: str) -> str:
    """
    Send a notice to OpenAI and return a concise summary.
    Clean, simple, easy to explain in interviews.
    """
    prompt = f"""You are a helpful assistant for college students.
Summarize the following notice in 4-5 bullet points.
Focus on: key information, deadlines, eligibility, and required actions.
Be concise and clear. Use plain language.

Notice Title: {title}

Notice Content:
{content}

Provide the summary as bullet points starting with •"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You summarize college notices concisely for students."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.3,  # Low temperature = more focused, less creative
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"OpenAI summarization failed: {e}")
        raise
