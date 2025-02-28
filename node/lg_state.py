from typing import TypedDict, Annotated, List
import operator
from .lg_llm import draft

class State(TypedDict):
    # get topic from user input
    topic: str
    # search news about specific topic
    websites_links: List[str]
    # parse the content of the websites
    websites_content: List[str]
    # draft the news for each website if successly parse
    websites_draft: Annotated[List[draft], operator.add]
    # combined draft
    combined_draft: str
    # image url
    news_image: str
    # s3 image url
    s3_image_url: str
    # news title
    news_title: str
    # save news to dynamodb
    save_success: bool
    
class WriterState(TypedDict):
    topic: str
    website_content: str
    websites_draft: Annotated[List[draft], operator.add]