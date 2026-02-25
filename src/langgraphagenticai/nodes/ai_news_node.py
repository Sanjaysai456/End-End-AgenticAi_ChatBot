import os
from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate


class AINewsNode:
    def __init__(self, llm):
        """
        Initialize the AINewsNode with API keys from environment variables.
        """

        tavily_api_key = os.getenv("TAVILY_API_KEY")

        if not tavily_api_key:
            raise ValueError("TAVILY_API_KEY not found in environment variables")

        # Explicitly pass key (more robust than implicit loading)
        self.tavily = TavilyClient(api_key=tavily_api_key)

        self.llm = llm
        self.state = {}

    def fetch_news(self, state: dict) -> dict:

        frequency = state['messages'][0].content.lower()
        self.state['frequency'] = frequency

        time_range_map = {'daily': 'd', 'weekly': 'w', 'monthly': 'm', 'year': 'y'}
        days_map = {'daily': 1, 'weekly': 7, 'monthly': 30, 'year': 366}

        if frequency not in time_range_map:
            raise ValueError("Invalid frequency selected")

        try:
            response = self.tavily.search(
                query="Top Artificial Intelligence (AI) technology news India and globally",
                topic="news",
                time_range=time_range_map[frequency],
                include_answer="advanced",
                max_results=20,
                days=days_map[frequency],
            )

            state['news_data'] = response.get('results', [])
            self.state['news_data'] = state['news_data']
            return state

        except Exception as e:
            raise RuntimeError(f"Error fetching news from Tavily: {e}")

    def summarize_news(self, state: dict) -> dict:

        news_items = self.state.get('news_data', [])

        if not news_items:
            raise ValueError("No news data found to summarize")

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Summarize AI news articles into markdown format. For each item include:
- Date in **YYYY-MM-DD** format in IST timezone
- Concise summary from latest news
- Sort news by date wise (latest first)
- Source URL as link

Use format:
### [Date]
- [Summary](URL)"""),
            ("user", "Articles:\n{articles}")
        ])

        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')}\n"
            f"URL: {item.get('url', '')}\n"
            f"Date: {item.get('published_date', '')}"
            for item in news_items
        ])

        response = self.llm.invoke(
            prompt_template.format(articles=articles_str)
        )

        state['summary'] = response.content
        self.state['summary'] = state['summary']

        return self.state

    def save_result(self, state):

        frequency = self.state.get('frequency', 'news')
        summary = self.state.get('summary', '')

        os.makedirs("./AINews", exist_ok=True)

        filename = f"./AINews/{frequency}_summary.md"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)

        self.state['filename'] = filename
        return self.state