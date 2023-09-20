import json
import os
import re
from typing import Any, List, Mapping, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
import requests
import langchain
from langchain.chains import ConversationChain, LLMChain, LLMMathChain, TransformChain, SequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.docstore import InMemoryDocstore
from langchain.llms.base import LLM, Optional, List, Mapping, Any
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import (
    ChatMessageHistory,
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
    ConversationSummaryBufferMemory
)
from langchain.prompts.prompt import PromptTemplate
from langchain.schema import messages_from_dict, messages_to_dict
from langchain.vectorstores import Chroma
from langchain.agents import load_tools
from langchain.agents import initialize_agent
import httpx

class CustomLLM(LLM):

    

    @property
    def _llm_type(self) -> str:
        return "custom"
    
    def _call(self, prompt: str, stop: List[str] | None = None, run_manager: CallbackManagerForLLMRun | None = None, history : List | None = None, **kwargs: Any) -> str:
        
        url = "http://localhost:5000/api/v1/chat"
        print(history)
        body ={
            "user_input": prompt,
            "max_new_tokens": 250,
            "auto_max_new_tokens": False,
            "history": history,
            "mode": "chat",
            "character": "Example",
            "instruction_template": "Vicuna-v1.1",
            "your_name": "You",
            "regenerate": False,
            "_continue": False,
            "stop_at_newline": False,
            "chat_generation_attempts": 1,
            "chat_instruct_command": "Continue the chat dialogue below. Write a single reply for the character "
        }
        data = json.dumps(body)
        headers = {"Content-Type": "application/json"}

        res = httpx.post(url=url, data=data, headers=headers,timeout=10.0)

        return res.text
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return super()._identifying_params