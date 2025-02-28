import os
from dotenv import load_dotenv,find_dotenv
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


if load_dotenv(find_dotenv(),override=True):
    logger.info("find .env file")
else:
    logger.warning("not find .env file")

# LLM
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Search
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")


# AWS
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")


missing_vars = []
for var_name in [
    "OPENAI_API_KEY", "GOOGLE_API_KEY", "GOOGLE_CSE_ID", 
    "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION", 
    "DYNAMODB_TABLE_NAME","OPENAI_API_KEY","DEEPSEEK_API_KEY"
]:
    if not locals().get(var_name):
        missing_vars.append(var_name)
        logger.warning(f"env variable {var_name} hasnt been set")

if not missing_vars:
    logger.info("all env variables are set")

