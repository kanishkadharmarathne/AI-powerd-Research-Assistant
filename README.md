# AI Research Assistant

An intelligent research assistant that leverages multiple LLMs and web search tools to gather and structure information.

## Features

- **Multiple LLM Support**: Google Gemini, OpenAI, Anthropic Claude
- **Web Search**: DuckDuckGo integration for real-time information
- **Wikipedia Integration**: Access structured knowledge articles
- **Structured Output**: Pydantic-based response validation

## Requirements

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Edit the `query` variable in `main.py` to search for different topics.

## Technologies

- **LangChain**: LLM orchestration framework
- **Google Gemini**: Primary LLM
- **Pydantic**: Data validation
- **DuckDuckGo Search**: Web search API
- **Wikipedia API**: Knowledge retrieval

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your API keys:
   ```
   GOOGLE_API_KEY=your_key_here
   ANTHROPIC_API_KEY= ""
   OPENAI_API_KEY=""
   ```
4. Run: `python main.py or streamlit run app.py`

## License

MIT
