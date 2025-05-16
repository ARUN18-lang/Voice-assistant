from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from utils import get_groq_api_key  

class Agent:
    def __init__(self):
        self.llm = ChatGroq(
            model="gemma2-9b-it",
            api_key=get_groq_api_key(),
            temperature=0.4,
            max_tokens=300,
        )
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant who answers questions and provides information. Keep your responses concise and clear for speech synthesis."),
            ("human", "{input}"),
        ])
    
    async def get_agent_response(self, input_text: str) -> str:
        if not input_text:
            return "I didn't receive any input. Please try again."
            
        chain = self.prompt_template | self.llm
        response = await chain.ainvoke({"input": input_text})
        
        return response.content
    
    async def cleanup(self):
        pass