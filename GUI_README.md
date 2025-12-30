# Voyager GUI Configuration Tool (PyQt6)

## Overview

The GUI tool (`gui.py`) provides a user-friendly interface for configuring Voyager's agent models and supported OpenAI Chat Completions parameters.

This version uses **PyQt6** (instead of Tkinter) and includes a premium-styled dark UI.

## Requirements

Install Python dependencies (including PyQt6):

```bash
pip install -r requirements.txt
```

> On Linux servers/headless environments you still need display access (e.g. X11/Wayland).

## Running the GUI

From the project directory:

```bash
python gui.py
```

## Tabs & behavior

### Models

Select the model used by each agent:

- Action agent
- Curriculum agent
- Curriculum QA
- Critic agent
- Skill manager

### Settings (new)

The **Settings** tab contains:

- `reasoning_effort`
- `verbosity`
- `store` (checkbox)

Model rules applied by the UI:

- **o1 / o3 / o4-mini**: only support `reasoning_effort` + `store` (verbosity is disabled)
- **gpt-5.2-pro**: only supports `store` (reasoning_effort + verbosity are disabled)
- **xhigh reasoning_effort**: only available when *all selected agent models* are `gpt-5.2`

### Old settings (legacy)

The **Old settings** tab is only available when **all selected agent models** are within the legacy range:

- starting at `gpt-3.5-turbo`
- ending at `gpt-4.1`

Old settings include:

- `temperature` (0.00 .. 2.00)
- `max_tokens` (0 .. model limit)
- `top_p` (0.00 .. 2.00)
- `store` (checkbox)

> If you select a mix of legacy and non-legacy models, the GUI will disable both Settings/Old settings and ask you to pick one family.

## Actions

- **Save config**: saves a JSON configuration file
- **Load config**: loads a previously saved JSON configuration file
- **Generate code**: generates a Python file that instantiates `Voyager` with your agent model selections
- **Reset**: returns everything to defaults

## Configuration file format

The GUI writes a JSON object like:

```json
{
  "action_agent": {"model": "gpt-4", "temperature": 0.0},
  "curriculum_agent": {
    "model": "gpt-4",
    "temperature": 0.0,
    "qa_model": "gpt-3.5-turbo",
    "qa_temperature": 0.0
  },
  "critic_agent": {"model": "gpt-4", "temperature": 0.0},
  "skill_manager": {"model": "gpt-3.5-turbo", "temperature": 0.0},
  "settings": {
    "reasoning_effort": "none",
    "verbosity": "medium",
    "store": false
  },
  "old_settings": {
    "temperature": 0.0,
    "top_p": 1.0,
    "max_tokens": 0,
    "store": false
  }
}
```

`example_usage.py` can load both this new format and the older legacy format.

## Troubleshooting

- **GUI window doesn't appear**: ensure you have display access (on Linux: `echo $DISPLAY`).
- **ImportError: PyQt6**: run `pip install -r requirements.txt`.
