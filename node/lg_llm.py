#from ..config.setting import OPENAI_API_KEY,DEEPSEEK_API_KEY
from config.setting import OPENAI_API_KEY,DEEPSEEK_API_KEY
from langchain_deepseek import ChatDeepSeek
from pydantic import BaseModel, Field
class draft(BaseModel):
    draft: str = Field(None, description="Draft of the news article.")

llm = ChatDeepSeek(model="deepseek-chat", api_key=DEEPSEEK_API_KEY)
llm_reasoning = ChatDeepSeek(model="deepseek-reasoner", api_key=DEEPSEEK_API_KEY)

writer_llm = llm.with_structured_output(draft)