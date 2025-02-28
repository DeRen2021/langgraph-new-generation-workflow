from openai import OpenAI
import logging
# from ..config.setting import OPENAI_API_KEY
from config.setting import OPENAI_API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)
model = "gpt-4o-mini"

def generate_news_image(news_text):
    """
    Generate a news image based on the news content.
    
    Args:
        news_text (str): The news article text
        
    Returns:
        str: URL of the generated image or None if failed
    """
    if not news_text:
        logger.error("No news text provided for image generation")
        return None
        
    logger.info("Starting news image generation process")
    
    # Truncate text to avoid token limits
    truncated_text = news_text[:500] + ("..." if len(news_text) > 500 else "")
    logger.debug(f"Truncated news text to {len(truncated_text)} characters")
    
    try:
        # 1. Generate image description using GPT
        logger.debug("Generating image description using language model")
        prompt_response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的新闻图片描述专家。请基于新闻内容，生成一个简短的图片描述（不超过100字），用于AI生成新闻配图。描述要具体且富有视觉细节。"
                },
                {
                    "role": "user",
                    "content": f"请为以下新闻生成简短的图片描述：\n\n{truncated_text}"
                }
            ],
            max_tokens=200  # 限制输出长度
        )
        
        image_prompt = prompt_response.choices[0].message.content
        logger.debug(f"Generated image description: '{image_prompt[:50]}...'")

        # 2. Use the prompt to generate an image
        logger.info("Generating image using DALL-E model")
        image_client = OpenAI(api_key=OPENAI_API_KEY)
        image_response = image_client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        image_url = image_response.data[0].url
        logger.info("Image generated successfully")
        logger.debug(f"Image URL: {image_url}")
        return image_url
        
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        if 'image_prompt' in locals():
            logger.error(f"Prompt used: {image_prompt}")
        return None
    
def generate_title(news_text: str) -> str:
    """
    Generate a title for news article using OpenAI.
    
    Args:
        news_text (str): The news article text
        
    Returns:
        str: Generated title or default message if failed
    """
    if not news_text:
        logger.error("No news text provided for title generation")
        return "Untitled News Article"
    
    logger.info("Starting title generation")
    
    try:
        # Truncate news text to avoid token limits
        truncated_text = news_text[:1000] + ("..." if len(news_text) > 1000 else "")
        logger.debug(f"Truncated news text to {len(truncated_text)} characters for title generation")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional news editor. Please generate a concise and appealing headline for the news content (within 20 characters)."
                },
                {
                    "role": "user",
                    "content": f"Please generate a headline for the following news:\n\n{truncated_text}"
                }
            ],
        )
        
        title = response.choices[0].message.content.strip()
        logger.info(f"Title generated successfully: '{title}'")
        return title
        
    except Exception as e:
        logger.error(f"Error generating title: {str(e)}")
        return "Untitled News Article"