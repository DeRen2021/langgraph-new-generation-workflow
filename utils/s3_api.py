import boto3
import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import logging

# from ..config.setting import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_REGION,AWS_BUCKET_NAME
from config.setting import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_REGION,AWS_BUCKET_NAME
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class S3Handler:
    def __init__(self):
        """
        maybe use aws config file for better security
        """
        logger.debug("Initializing S3Handler")
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_REGION
            )
            self.bucket_name = AWS_BUCKET_NAME
            logger.info(f"S3Handler initialized for bucket: {self.bucket_name} in region: {AWS_REGION}")
        except Exception as e:
            logger.error(f"Failed to initialize S3 client: {str(e)}")
            raise

    def upload_image(self, image_url: str, s3_key: str, date_str: str = None) -> str:
        """
        从URL下载图片并上传到S3
        
        Args:
            image_url (str): 图片的URL
            s3_key (str): 在S3中保存的文件路径和名称
            date_str (str, optional): 日期字符串，用于文件夹组织

        Returns:
            str: S3中的公开访问URL
        """
        if not image_url:
            logger.error("No image URL provided")
            return None
            
        logger.info(f"Attempting to upload image from {image_url} to S3")
        
        try:
            # 下载图片
            logger.debug(f"Downloading image from {image_url}")
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            image_content = response.content
            content_type = response.headers.get('content-type', 'image/jpeg')
            
            logger.debug(f"Image downloaded successfully: {len(image_content)} bytes, type: {content_type}")

            # 确保s3_key格式正确
            if not s3_key.startswith('images/'):
                original_key = s3_key
                s3_key = f"images/{s3_key}"
                logger.debug(f"Modified S3 key from {original_key} to {s3_key}")

            # 上传到S3，移除ACL参数
            logger.debug(f"Uploading to S3 bucket {self.bucket_name} with key {s3_key}")
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=image_content,
                ContentType=content_type
            )

            # 生成公开访问的URL
            region = AWS_REGION
            if region == 'us-east-1':
                url = f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"
            else:
                url = f"https://{self.bucket_name}.s3.{region}.amazonaws.com/{s3_key}"

            logger.info(f"Image uploaded successfully to S3: {url}")
            return url

        except requests.RequestException as e:
            logger.error(f"Failed to download image from {image_url}: {str(e)}")
            return None
        except boto3.exceptions.S3UploadFailedError as e:
            logger.error(f"S3 upload failed for key {s3_key}: {str(e)}")
            return None
        except boto3.exceptions.Boto3Error as e:
            logger.error(f"AWS S3 error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error uploading image to S3: {str(e)}", exc_info=True)
            return None

    def get_public_url(self, s3_key: str) -> str:
        """
        获取S3对象的公开访问URL
        
        Args:
            s3_key (str): S3对象的键值

        Returns:
            str: 公开访问URL
        """
        if not s3_key:
            logger.warning("Empty S3 key provided to get_public_url")
            return None
            
        logger.debug(f"Generating public URL for S3 key: {s3_key}")
        
        region = AWS_REGION
        if region == 'us-east-1':
            url = f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"
        else:
            url = f"https://{self.bucket_name}.s3.{region}.amazonaws.com/{s3_key}"
            
        logger.debug(f"Generated URL: {url}")
        return url