<h1 align="center">
  Slack Research Agent
</h1>

<h3 align="center">
Build AI Research Agent using Langchain and integrate it with Slack
</h3>

## About this project

This project demonstrates how to create a powerful tool designed to provide users with quick and accurate summaries of information about the company website mentioned in Slack channels. Leveraging LangChain, this agent uses Wikipedia and web search tools(I have used Tavily because it's free and easy to generate API keys, you could replace it with Bing, Google, etc.) to gather and summarize relevant data efficiently.

### Prerequisites

1. Python 3.9 or higher installed on your system.
2. Slack account.

### Slack Setup

It is important to configure your Slack bot correctly for this code to work.

#### Step 1: Create a Slack Account

1. **Sign Up or Log In**:
   - Visit [Slack app page](https://api.slack.com/apps).
   - If you don't have an account, sign up. Otherwise, log in with your existing credentials.

#### Step 2: Configure Slack

1. **Create a Slack App**:
   - Click **Create New App**
   - Select **From Scratch**
   - Enter an **App Name** and select the workspace(You can choose Slack if you do not have a workspace)
   - Click **Create App**
  Once the app is created successfully you will be redirected to **Basic Information** page.
  
2. **Configure Scope**:
   - Navigate to **OAuth & Permissions** under **Features** section.
   - Go to **Bot Token Scopes** in the **Scope** section, click **Add an OAuth Scope**
   - Add scopes "chat:write" and "chat:write.public"
  
3. **Install App**:
   - Click **Install to Workspace** button on the **OAuth & Permissions** page under **OAuth Tokens for Your Workspace** section.
   - Click **Allow** and you will be redirected to the **OAuth & Permissions** page again
   - Copy the **Bot User OAuth Token** and save it in your .env file as SLACK_BOT_TOKEN
  
4. **Get Slack App Token**:
   - Go to **Basic information** under **Settings**
   - Navigate to **App-Level Tokens** and click **Generate Token and Scopes**
   - Enter a token name, click **Add Scope**
   - Add the scope "connections:write" and click **Generate**
   - Copy the **Token** and save it in your .env file as SLACK_APP_TOKEN

3. **Final Settings**:
   - Navigate to **Socket Mode** under **Settings** section.
   - Toggle **Enable Socket Mode** on
   - Navigate to **Interactivity & Shortcuts** under **Features** section.
   - Toggle **Interactivity** on
   - Navigate to **Event Subscriptions** under **Features** section.
   - Toggle **Enable Events** on
   - Click **Subscribe to bot events>Add Bot User Event**
   - Add events "message.im" and "app_mention"
   - Click **Save Changes* at the bottom
   - Click on **Reinstall your app** that appears on the banner
   - Click *Allow*

Yup, that's it we are done!!
     
### Environment Setup

1. **Create a Virtual Environment**: 
   This isolates your Python setup on a per-project basis.
   - Create a virtual environment using:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - For Linux or macOS:
       ```bash
       source venv/bin/activate
       ```
     - For Windows:
       ```bash
       venv\Scripts\activate
       ```

2. **Install Dependencies**:
   - Install the required libraries. Run the command:
     ```bash
     pip install requests langchain_openai langchain_core python-dotenv langchain_community langchainhub
     ```

3. **Environment Variables**: 
   - Set up variable in a `.env` file in the script's directory:
     ```
     OPENAI_API_KEY=your_openai_api_key
     SLACK_BOT_TOKEN=your_slack_bot_token
     SLACK_APP_TOKEN=your_slack_app_token
     TAVILY_API_KEY=your_serper_api_key
     ```

### Get those agents to work

1. **Run the app**:
   - Run the app:
     ```bash
     python app.py
     ```

2. **Run agents on Slack**
   - Open your Slack app
   - In the **Apps** section you should have your app
   - Click on the app and provide it with the company's website you want to analyze
   - Sit back and let the bot analyze

#### Notes

- Handle API keys and configurations carefully to maintain script functionality.
- Test changes in a controlled environment before deployment.

This README provides comprehensive instructions for customization and usage of the script. Enjoy coding!
