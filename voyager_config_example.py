"""Example Voyager configuration.

This file is similar to what the GUI's "Generate code" action produces.
"""

from voyager import Voyager

openai_api_key = "YOUR_OPENAI_API_KEY"

azure_login = {
    "client_id": "YOUR_CLIENT_ID",
    "redirect_url": "https://127.0.0.1/auth-response",
    "secret_value": "[OPTIONAL] YOUR_SECRET_VALUE",
    "version": "fabric-loader-0.14.18-1.19",
}

voyager = Voyager(
    azure_login=azure_login,
    openai_api_key=openai_api_key,
    action_agent_model_name="gpt-4",
    action_agent_temperature=0.0,
    curriculum_agent_model_name="gpt-4",
    curriculum_agent_temperature=0.0,
    curriculum_agent_qa_model_name="gpt-3.5-turbo",
    curriculum_agent_qa_temperature=0.0,
    critic_agent_model_name="gpt-4",
    critic_agent_temperature=0.0,
    skill_manager_model_name="gpt-3.5-turbo",
    skill_manager_temperature=0.0,
)

# Additional Chat Completions API options (LangChain ChatOpenAI kwargs)
chat_completions_options = {
    "store": False,
    "top_p": 1.0,
    "max_tokens": 0,
}

# voyager.learn()
