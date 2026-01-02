from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from tools import search_tool, wiki_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            you are a research assistant that will help you generate a research paper.
            answer the user query and gather information.
            wrap the output in this format and provide no other text\n{format_instructions}""",
        ),
        ("human", "{query}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool ]
chain = prompt | llm | tools

query = "sri lanka?"
response = chain.invoke({"query": query})

try:
    structured_response = parser.parse(response.content)
    print("Structured Response:", structured_response)
except Exception as e:
    print("Error parsing response:", e," response content:", response.content)

