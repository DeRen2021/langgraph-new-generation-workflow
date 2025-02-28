# from ..utils.web_search import search
# from ..utils.web_parse import fetch_and_extract
# from ..utils.pic_generator import generate_news_image, generate_title
# from ..utils.s3_api import S3Handler
# from ..utils.dynamodb_api import DynamoDBHandler
# from .lg_state import State, WriterState
# from .lg_llm import writer_llm,llm
from utils.web_search import search
from utils.web_parse import fetch_and_extract
from utils.pic_generator import generate_news_image, generate_title
from utils.s3_api import S3Handler
from utils.dynamodb_api import DynamoDBHandler
from .lg_state import State, WriterState
from .lg_llm import writer_llm,llm
from langgraph.constants import Send
from datetime import datetime, timezone, timedelta

import asyncio
import nest_asyncio

from config.topic import TOPICS

tz = timezone(timedelta(hours=8))
today_date = datetime.now(tz).date().isoformat()

def web_search(state: State):
    """Search the web for the topic."""
    try:
        results = search("news about " + state["topic"])
    except Exception as e:
        raise e

    return {"websites_links": [result.link for result in results]}


def web_parse(state: State):
    """Parse the web content."""
    nest_asyncio.apply()
    
    try:
        contents = asyncio.run(fetch_and_extract(state["websites_links"]))
    except RuntimeError:
        loop = asyncio.get_event_loop()
        contents = loop.run_until_complete(fetch_and_extract(state["websites_links"]))

    #print(contents)
    return {"websites_content": contents}

def draft_news(state: WriterState):
    """Draft the news."""
    try:
        draft = writer_llm.invoke(f"Draft a news article about {state['topic']} based on the following content: {state['website_content']}")
        return {"websites_draft": [draft.draft]}
    except Exception as e:
        return {"websites_draft": [None]}
    

def combine_news(state: State):
    """Combine the news."""

    # Format completed section to str to use as context for final sections
    #print("debug:" ,"inside combine_news")
    state["websites_draft"] = [s for s in state["websites_draft"] if s is not None]
    website_draft = "\n".join(state["websites_draft"])[:10000]
    #:" ,website_draft)
    combined_draft = llm.invoke(f"Combine the following news articles into a single news article: {website_draft}")

    return {"combined_draft": combined_draft.content}

def assign_writer(state: State):
    """Assign a worker to each section in the plan"""
    # Kick off section writing in parallel via Send() API
    return [Send("draft_news", {"website_content": wc, "topic": state["topic"]}) for wc in state["websites_content"] if wc != None]

def generate_news_image_node(state: State):
    """Generate a news image."""
    image_url = generate_news_image(state["combined_draft"])
    return {"news_image": image_url}

def save_image_to_s3(state: State):
    """Save the news to S3."""
    s3_key = f"images/{state['topic']}/{today_date}.jpg"
    s3_handler = S3Handler()
    s3_url = s3_handler.upload_image(state["news_image"], s3_key,today_date)
    print("test1",s3_url)
    return {"s3_image_url": s3_url}


def generate_news_title(state: State):
    """Generate a news title."""
    title = generate_title(state["combined_draft"])
    return {"news_title": title}

def save_news_to_dynamodb(state: State):
    db_handler = DynamoDBHandler()
    import time
    time.sleep(5)
    
    # 使用get方法提供默认值
    s3_image_url = state.get('s3_image_url')
    topic_name = [i["name"]  for i in TOPICS if i["id"] == state["topic"] ]
    #print("debug: s3_image_url =", s3_image_url)
    
    save_success = db_handler.save_article(
        topic_id=state["topic"],
        topic_name=topic_name,
        date=today_date,
        title=state["news_title"],
        content=state['combined_draft'],
        web_links="\n".join(state['websites_links']),
        image_url=s3_image_url  
    )
    return {"save_success": save_success}



