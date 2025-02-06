import openai
from fastapi import HTTPException
from dotenv import load_dotenv
import os

# Load API key from environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = "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"



async def generate_blog_post(topic: str) -> dict:
    """
    Generate a blog post using the AI agent.
    """
    try:
        # Use ChatCompletion for chat models like gpt-4o-mini
        response = await openai.ChatCompletion.acreate(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant that writes detailed blog posts."},
                {"role": "user", "content": f"Write a detailed blog post about {topic}."}
            ],
            max_tokens=800,
            temperature=0.7,
        )
        
        # Extract the generated text from the response
        blog_post_content = response['choices'][0]['message']['content'].strip()

        # Return the content as a dictionary with title and content
        return {"title": topic, "content": blog_post_content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate blog post: {str(e)}")