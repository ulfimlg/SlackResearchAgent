import os
from dotenv import load_dotenv
from langchain_community.tools import WikipediaQueryRun, BraveSearch
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import AgentExecutor, load_tools, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import SystemMessagePromptTemplate, PromptTemplate
from langchain import hub
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Load environment variables
load_dotenv()

# Define functions
def load_api_keys():
    """Load API keys from environment variables."""
    os.environ['OPENAI_API_KEY'] = os.getenv("MY_OPENAI_API_KEY")
    os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
    brave_api_key = os.getenv("BRAVE_SEARCH_API")
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    return brave_api_key, slack_token

def setup_tools(brave_api_key):
    """Set up tools for the agent."""
    search_tool = BraveSearch.from_api_key(api_key=brave_api_key, search_kwargs={"count": 3})
    tavily_search_tool = TavilySearchResults()
    wolfram = load_tools(["wolfram-alpha"])
    api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
    wiki = WikipediaQueryRun(api_wrapper=api_wrapper)
    tools = [wiki, wolfram[0], tavily_search_tool]
    return tools

def setup_agent(tools):
    """Set up the agent with tools and prompt."""
    template = """
    Task: Comprehensive Account Plan

    Instructions:

    As a senior research analyst at Gartner, your objective is to create a detailed account plan for the business specified in the provided URL. Your report should include the following sections:

    1) Business Model: Provide a single sentence summary explaining how the business operates and generates revenue.
    2) Product Portfolio: List key products and services, each with a single sentence description.
    3) Sales Channels: Enumerate the publicly available sales channels.
    4) Company Financials: List key financial metrics, including current year and past years sales, profit, funding raised(if aplicable) and share price if the company is publicly traded by analyzing websites from web search using BraveSearch. Calculate the growth rate for sales and profit using wolfram-alpha if data is available.
    5) Customer Support: Identify the main customer support channels, each with a single sentence description.
    6) Sustainability Initiatives: List the company's sustainability initiatives, each with a single sentence description.
    7) Recent News Articles and Events: Summarize recent news articles and events related to the company.
    8) Key Personnel: Include names and titles of sales leaders (Head of Sales, Head of Business Development), CIO, and Sales Operations personnel.

    Guidelines:

    * Begin your research on Wikipedia, then use brave_search for additional information. Provided we have data utilize Wolfram Alpha for any calculations.
    * Cite a reference and source link for each point mentioned. Provide references in each section Business Model, Product Portfolio, Sales Channels, Company Financials, Customer Support, Sustainability Initiatives, Recent News Articles and Events, and Key Personnel.
    * Format your response using headings and bullet points.
    * Ensure the output is in plain text format, avoiding markdown.

    """

    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    prompt = hub.pull("hwchase17/openai-functions-agent")
    prompt.messages[0] = SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], template=template))
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor

def setup_slack_app(slack_token, agent_executor):


    """Set up the Slack app and message handler."""
    app = App(token=slack_token)

    @app.message(".*")
    def message_handler(message, say, logger):
        """Handle incoming messages from Slack."""
        print(message)
        say(f"Researching {message['text']} for you...")
        output = agent_executor.invoke({"input": message['text']})
        say(output['output'])

    @app.event("app_mention")
    def handle_app_mention_events(message, body, logger):
        """Handle app mention events."""
        logger.info(body)

    return app

def main():
    """Main function to run the application."""
    brave_api_key, slack_token = load_api_keys()
    tools = setup_tools(brave_api_key)
    agent_executor = setup_agent(tools)
    app = setup_slack_app(slack_token, agent_executor)
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

if __name__ == "__main__":
    main()
