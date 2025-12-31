"""Example Voyager configuration.

This file is similar to what the GUI's "Generate code" action produces.
"""

from voyager import Voyager

openai_api_key = "YOUR_OPENAI_API_KEY"

# Minecraft in-game port
# To get the port:
# 1. Start Minecraft and create a world
# 2. Set Game Mode to Creative and Difficulty to Peaceful
# 3. Press Esc and select "Open to LAN"
# 4. Enable "Allow cheats: ON" and press "Start LAN World"
# 5. Copy the port number from the chat
mc_port = 25565  # Replace with your actual port

voyager = Voyager(
    mc_port=mc_port,
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
