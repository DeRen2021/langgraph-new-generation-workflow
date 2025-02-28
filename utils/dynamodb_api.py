import boto3
from datetime import datetime
import logging
from dotenv import load_dotenv
# from ..config.setting import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_REGION,DYNAMODB_TABLE_NAME
from config.setting import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_REGION,DYNAMODB_TABLE_NAME
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DynamoDBHandler:
    def __init__(self):
        """
        Initialize DynamoDB handler with AWS credentials from settings
        """
        logger.debug("Initializing DynamoDBHandler")
        try:
            self.dynamodb = boto3.resource(
                'dynamodb',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_REGION
            )
            self.table_name = DYNAMODB_TABLE_NAME
            self.table = self.dynamodb.Table(self.table_name)
            logger.info(f"DynamoDBHandler initialized for table: {self.table_name} in region: {AWS_REGION}")
        except Exception as e:
            logger.error(f"Failed to initialize DynamoDB client: {str(e)}")
            raise

    def save_article(self, topic_id: str, topic_name: str, date: str, title: str, 
                    content: str, web_links: list, image_url: str = None) -> bool:
        """
        保存文章到DynamoDB
        
        Args:
            topic_id (str): 主题ID
            topic_name (str): 主题名称
            date (str): 日期
            title (str): 文章标题
            content (str): 文章内容
            web_links (list): 参考网站链接列表
            image_url (str, optional): S3图片URL

        Returns:
            bool: 是否保存成功
        """
        # Validate required inputs
        if not all([topic_id, date, title, content]):
            logger.error("Missing required fields for article save")
            return False
            
        logger.info(f"Saving article with topic_id: {topic_id}, title: '{title[:30]}...'")
        
        try:
            # Prepare item for DynamoDB
            item = {
                'topic_id': topic_id,
                'date': date,
                'title': title,
                'content': content,
                'topic_name': topic_name,
                'web_links': web_links if web_links else [],
                'created_at': datetime.now().isoformat()
            }
            
            if image_url:
                logger.debug(f"Article includes image URL: {image_url}")
                item['image_url'] = image_url
            
            # Content size logging
            content_size = len(content)
            logger.debug(f"Article content size: {content_size} characters")
            
            # Save to DynamoDB
            logger.debug(f"Putting item into DynamoDB table: {self.table_name}")
            self.table.put_item(Item=item)
            
            logger.info(f"Successfully saved article '{title[:30]}...' to DynamoDB")
            return True

        except boto3.exceptions.Boto3Error as e:
            # Handle specific AWS errors
            logger.error(f"AWS DynamoDB error while saving article: {str(e)}")
            return False
        except Exception as e:
            # Handle other unexpected errors
            logger.error(f"Failed to save article to DynamoDB: {str(e)}", exc_info=True)
            return False
            
    def get_article(self, topic_id: str, date: str) -> dict:
        """
        从DynamoDB获取文章
        
        Args:
            topic_id (str): 主题ID
            date (str): 日期
            
        Returns:
            dict: 文章数据，获取失败则返回None
        """
        if not topic_id or not date:
            logger.error("Missing required parameters for article retrieval")
            return None
            
        logger.info(f"Retrieving article with topic_id: {topic_id}, date: {date}")
        
        try:
            response = self.table.get_item(
                Key={
                    'topic_id': topic_id,
                    'date': date
                }
            )
            
            if 'Item' in response:
                logger.info(f"Article found and retrieved successfully")
                return response['Item']
            else:
                logger.warning(f"No article found with topic_id: {topic_id}, date: {date}")
                return None
                
        except boto3.exceptions.Boto3Error as e:
            logger.error(f"AWS DynamoDB error while retrieving article: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve article from DynamoDB: {str(e)}")
            return None 