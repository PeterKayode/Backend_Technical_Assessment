import openai
from fastapi import HTTPException
from dotenv import load_dotenv
import os
import traceback


# Load API key from environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = "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"


async def generate_blog_post(title: str, topic: str) -> dict:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant that writes detailed blog posts."},
                {"role": "user", "content": f"Write a detailed blog post about {topic}."}
            ],
            max_tokens=800,
            temperature=0.7,
        )

        blog_post_content = response['choices'][0]['message']['content'].strip()

        return {"title": title, "content": blog_post_content}

    except Exception as e:
        error_message = f"Failed to generate blog post: {str(e)}"
        traceback_details = traceback.format_exc()  # Capture the full traceback
        print(f"{error_message}\nTraceback:\n{traceback_details}")  # Print both
        raise HTTPException(status_code=500, detail=error_message)