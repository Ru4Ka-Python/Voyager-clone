# Voyager GUI Configuration Tool

## Overview

The GUI tool (`gui.py`) provides a user-friendly interface for configuring Voyager's GPT models and Chat Completions API parameters without editing code directly.

## Requirements

The GUI uses Python's built-in `tkinter` library. On most Python installations, this is included by default. If you encounter an error about `tkinter` not being found:

### Ubuntu/Debian
```bash
sudo apt-get install python3-tk
```

### macOS
Tkinter is included with the official Python installer. If you're using Homebrew:
```bash
brew install python-tk
```

### Windows
Tkinter is included with the standard Python installer.

## Running the GUI

Simply run the GUI from the project directory:

```bash
python gui.py
```

## Features

### Models Tab

Configure the GPT model for each agent:

| Agent | Description | Default Model |
|-------|-------------|---------------|
| Action Agent | Generates code to complete tasks | gpt-4 |
| Curriculum Agent | Proposes new learning tasks | gpt-4 |
| Curriculum QA | Answers questions for task context | gpt-3.5-turbo |
| Critic Agent | Evaluates task completion | gpt-4 |
| Skill Manager | Manages skill retrieval and storage | gpt-3.5-turbo |

**Available Models:**
- gpt-5.2-pro, gpt-5.2, gpt-5.1, gpt-5-mini
- gpt-4.1, gpt-4.1-mini
- o4-mini, o3, o1
- gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-4
- gpt-3.5-turbo

### Options Tab

Configure Chat Completions API parameters:

- **Reasoning Effort**: Controls the depth of reasoning in responses
  - `none`: No additional reasoning (default)
  - `low`: Minimal reasoning
  - `medium`: Balanced reasoning
  - `high`: Deep reasoning
  - `xhigh`: Maximum reasoning

- **Verbosity**: Controls output verbosity
  - `low`: Minimal output
  - `medium`: Balanced output (default)
  - `high`: Detailed output

- **Store**: Whether to store conversation history
  - `false`: Do not store (default)
  - `true`: Store conversations

### Advanced Tab

- **Temperature**: Controls randomness in responses (0.0 - 2.0)
  - Lower values (0.0 - 0.3): More deterministic, focused
  - Medium values (0.4 - 0.7): Balanced creativity
  - Higher values (0.8 - 2.0): More creative, varied

## Actions

### Save Config
Saves your current configuration to a JSON file that can be loaded later.

### Generate Code
Generates a Python script with your selected configuration. The script includes:
- All model settings
- Temperature settings
- Chat Completions API options
- Template for Azure login and OpenAI API key

### Load Config
Loads a previously saved JSON configuration file.

### Reset
Resets all settings to their default values.

### Exit
Closes the GUI.

## Workflow Example

1. **Launch the GUI**: `python gui.py`
2. **Select Models**: Choose appropriate models for each agent based on your needs and budget
3. **Configure Options**: Set reasoning effort, verbosity, and store preferences
4. **Save or Generate Code**:
   - **Save Config**: Saves a JSON file that can be loaded later (e.g., `my_config.json`)
   - **Generate Code**: Generates a Python script with your configuration (e.g., `voyager_config.py`)
5. **Edit Configuration**: Open the generated file and add your credentials:
   ```python
   openai_api_key = "sk-your-api-key-here"
   azure_login = {
       "client_id": "your-client-id",
       "redirect_url": "https://127.0.0.1/auth-response",
       "secret_value": "optional-secret",
       "version": "fabric-loader-0.14.18-1.19",
   }
   ```
6. **Run Voyager**:
   - For generated Python scripts:
     ```bash
     python voyager_config.py
     ```
   - For JSON configurations, use the provided loader:
     ```python
     from example_usage import load_voyager_from_config
     voyager, options = load_voyager_from_config("my_config.json")
     voyager.learn()
     ```

## Configuration File Format

The JSON configuration file uses this structure:

```json
{
    "action_agent": {
        "model": "gpt-4",
        "temperature": 0.0
    },
    "curriculum_agent": {
        "model": "gpt-4",
        "temperature": 0.0,
        "qa_model": "gpt-3.5-turbo",
        "qa_temperature": 0.0
    },
    "critic_agent": {
        "model": "gpt-4",
        "temperature": 0.0
    },
    "skill_manager": {
        "model": "gpt-3.5-turbo",
        "temperature": 0.0
    },
    "reasoning_effort": "none",
    "verbosity": "medium",
    "store": "false"
}
```

## Tips

1. **Cost vs. Performance**: Use gpt-3.5-turbo for agents that don't require complex reasoning (like QA and skill management) to reduce costs.

2. **Reasoning Effort**: Higher reasoning effort may improve task success but increases API costs and response time.

3. **Temperature**: Set to 0 for deterministic behavior (recommended for production). Increase for more experimentation.

4. **Save Configurations**: Save different configurations for different use cases (e.g., `config_experimental.json`, `config_production.json`).

## Troubleshooting

### Tkinter not found
Install the tkinter package for your OS (see Requirements above).

### GUI window doesn't appear
Make sure you're running the command from the project directory and that you have display access (on Linux, check `echo $DISPLAY`).

### Generated code doesn't run
Ensure you've replaced the placeholder values for `openai_api_key` and `azure_login` with your actual credentials.

## License

This GUI tool is part of the Voyager project and is licensed under the MIT License.
