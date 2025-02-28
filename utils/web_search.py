import requests
from dataclasses import dataclass
import logging
from typing import List
# from ..config.setting import GOOGLE_API_KEY,GOOGLE_CSE_ID
from config.setting import GOOGLE_API_KEY,GOOGLE_CSE_ID

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



GOOGLE_API_BASE_URL = 'https://www.googleapis.com/customsearch/v1'
DEFAULT_DATE_RESTRICT = 'd1'  


@dataclass
class SearchResult:
    title: str
    link: str
    snippet: str


class GoogleSearchClient:

    
    def __init__(self):
        self.api_key = GOOGLE_API_KEY
        self.cse_id = GOOGLE_CSE_ID
        
        # if not self.api_key or not self.cse_id:
        #     logger.error("未找到Google API凭证")
        #     raise ValueError("Google API credentials not found in environment variables")
    
    def search(self, query: str, date_restrict: str = DEFAULT_DATE_RESTRICT, 
               num_results: int = 2, start_index: int = 1) -> List[SearchResult]:
        """执行Google搜索并返回结果。
        
        Args:
            query: 搜索查询词
            date_restrict: 日期限制 (例如: 'd1'表示过去一天)
            num_results: 返回的最大结果数
            start_index: 结果的起始索引（用于分页）
            
        Returns:
            搜索结果列表
            
        Raises:
            ValueError: 如果API凭证无效
            RequestException: 如果API请求失败
        """
        params = {
            'key': self.api_key,
            'cx': self.cse_id,
            'q': query,
            'dateRestrict': date_restrict,
            'num': num_results,
            'start': start_index
        }
        
        try:
            response = requests.get(GOOGLE_API_BASE_URL, params=params, timeout=10)
            response.raise_for_status() 
            
            results_list = []
            results = response.json().get('items', [])
            
            for item in results:
                # Maybe add addtion log here for robustness and debug
                result = SearchResult(
                    title=item.get('title', ''),
                    link=item.get('link', ''),
                    snippet=item.get('snippet', '')
                )
                results_list.append(result)
            
            logger.info(f"search success '{query}', find {len(results_list)} results")
            return results_list
            
        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.ConnectionError):
                logger.error(f"connection error: {str(e)}")
            elif isinstance(e, requests.exceptions.Timeout):
                logger.error(f"timeout error: {str(e)}")
            else:
                logger.error(f"google search error: {str(e)}")

def search(topic: str) -> List[SearchResult]:
    """执行Google搜索的旧函数（为了向后兼容）。
    
    Args:
        topic: 搜索查询词
        
    Returns:
        搜索结果列表
    """
    client = GoogleSearchClient()
    return client.search(query=topic)