#!/usr/bin/env python3
"""
GUI for selecting GPT models and parameters for Voyager.

This tool provides a graphical interface to configure Voyager's LLM settings,
including model selection, reasoning effort, verbosity, and storage options.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os


class VoyagerConfigGUI:
    """GUI for configuring Voyager's GPT model settings."""

    MODELS = [
        "gpt-5.2-pro",
        "gpt-5.2",
        "gpt-5.1",
        "gpt-5-mini",
        "gpt-4.1",
        "gpt-4.1-mini",
        "o4-mini",
        "o3",
        "o1",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-4",
        "gpt-3.5-turbo",
    ]

    REASONING_EFFORT = ["none", "low", "medium", "high", "xhigh"]
    VERBOSITY = ["low", "medium", "high"]
    STORE = ["true", "false"]

    def __init__(self, root):
        self.root = root
        self.root.title("Voyager GPT Model Configuration")
        self.root.geometry("700x550")
        self.root.resizable(False, False)

        self.config = self._create_default_config()

        self._setup_ui()

    def _create_default_config(self):
        """Create default configuration."""
        return {
            "action_agent": {
                "model": "gpt-4",
                "temperature": 0,
            },
            "curriculum_agent": {
                "model": "gpt-4",
                "temperature": 0,
                "qa_model": "gpt-3.5-turbo",
                "qa_temperature": 0,
            },
            "critic_agent": {
                "model": "gpt-4",
                "temperature": 0,
            },
            "skill_manager": {
                "model": "gpt-3.5-turbo",
                "temperature": 0,
            },
            "reasoning_effort": "none",
            "verbosity": "medium",
            "store": "false",
        }

    def _setup_ui(self):
        """Set up the user interface."""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._create_model_selection_tab(notebook)
        self._create_options_tab(notebook)
        self._create_advanced_tab(notebook)

        self._create_buttons()

    def _create_model_selection_tab(self, notebook):
        """Create the model selection tab."""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Models")

        frame = ttk.Frame(tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        row = 0
        ttk.Label(frame, text="Action Agent Model", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        self.action_agent_model = ttk.Combobox(
            frame, values=self.MODELS, state="readonly", width=30
        )
        self.action_agent_model.set(self.config["action_agent"]["model"])
        self.action_agent_model.grid(row=row, column=1, pady=5, padx=10)

        row += 1
        ttk.Label(frame, text="Curriculum Agent Model", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        self.curriculum_agent_model = ttk.Combobox(
            frame, values=self.MODELS, state="readonly", width=30
        )
        self.curriculum_agent_model.set(self.config["curriculum_agent"]["model"])
        self.curriculum_agent_model.grid(row=row, column=1, pady=5, padx=10)

        row += 1
        ttk.Label(frame, text="Curriculum QA Model", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        self.curriculum_qa_model = ttk.Combobox(
            frame, values=self.MODELS, state="readonly", width=30
        )
        self.curriculum_qa_model.set(self.config["curriculum_agent"]["qa_model"])
        self.curriculum_qa_model.grid(row=row, column=1, pady=5, padx=10)

        row += 1
        ttk.Label(frame, text="Critic Agent Model", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        self.critic_agent_model = ttk.Combobox(
            frame, values=self.MODELS, state="readonly", width=30
        )
        self.critic_agent_model.set(self.config["critic_agent"]["model"])
        self.critic_agent_model.grid(row=row, column=1, pady=5, padx=10)

        row += 1
        ttk.Label(frame, text="Skill Manager Model", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        self.skill_manager_model = ttk.Combobox(
            frame, values=self.MODELS, state="readonly", width=30
        )
        self.skill_manager_model.set(self.config["skill_manager"]["model"])
        self.skill_manager_model.grid(row=row, column=1, pady=5, padx=10)

    def _create_options_tab(self, notebook):
        """Create the options tab."""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Options")

        frame = ttk.Frame(tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        row = 0
        ttk.Label(frame, text="Reasoning Effort", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=15
        )
        self.reasoning_effort = ttk.Combobox(
            frame, values=self.REASONING_EFFORT, state="readonly", width=20
        )
        self.reasoning_effort.set(self.config["reasoning_effort"])
        self.reasoning_effort.grid(row=row, column=1, pady=15, padx=10)

        row += 1
        ttk.Label(frame, text="Verbosity", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=15
        )
        self.verbosity = ttk.Combobox(
            frame, values=self.VERBOSITY, state="readonly", width=20
        )
        self.verbosity.set(self.config["verbosity"])
        self.verbosity.grid(row=row, column=1, pady=15, padx=10)

        row += 1
        ttk.Label(frame, text="Store", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=15
        )
        self.store = ttk.Combobox(
            frame, values=self.STORE, state="readonly", width=20
        )
        self.store.set(self.config["store"])
        self.store.grid(row=row, column=1, pady=15, padx=10)

        row += 1
        ttk.Label(
            frame,
            text="Note: These options control the behavior of the Chat Completions API.",
            font=("Arial", 9, "italic"),
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=20)

    def _create_advanced_tab(self, notebook):
        """Create the advanced settings tab."""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Advanced")

        frame = ttk.Frame(tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        row = 0
        ttk.Label(frame, text="Temperature", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        self.temperature_var = tk.DoubleVar(value=0.0)
        self.temperature_scale = ttk.Scale(
            frame,
            from_=0.0,
            to=2.0,
            variable=self.temperature_var,
            orient=tk.HORIZONTAL,
            length=200,
        )
        self.temperature_scale.grid(row=row, column=1, pady=5, padx=10)
        self.temperature_label = ttk.Label(frame, text="0.0")
        self.temperature_label.grid(row=row, column=2, padx=5)
        self.temperature_scale.configure(
            command=lambda v: self.temperature_label.configure(text=f"{float(v):.1f}")
        )

        row += 1
        ttk.Label(
            frame,
            text="Temperature controls randomness. Lower is more deterministic.",
            font=("Arial", 9, "italic"),
        ).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=5)

        row += 1
        ttk.Button(
            frame, text="Apply Same Temperature to All Agents", command=self._apply_temperature_all
        ).grid(row=row, column=0, columnspan=3, pady=10)

    def _create_buttons(self):
        """Create action buttons."""
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(button_frame, text="Save Config", command=self._save_config).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(button_frame, text="Generate Code", command=self._generate_code).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(button_frame, text="Load Config", command=self._load_config).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(button_frame, text="Reset", command=self._reset).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(
            side=tk.RIGHT, padx=5
        )

    def _apply_temperature_all(self):
        """Apply the temperature to all agents."""
        temp = self.temperature_var.get()
        self.config["action_agent"]["temperature"] = temp
        self.config["curriculum_agent"]["temperature"] = temp
        self.config["curriculum_agent"]["qa_temperature"] = temp
        self.config["critic_agent"]["temperature"] = temp
        self.config["skill_manager"]["temperature"] = temp
        messagebox.showinfo("Applied", f"Temperature {temp:.1f} applied to all agents")

    def _get_config_from_ui(self):
        """Get configuration from UI elements."""
        config = self._create_default_config()
        config["action_agent"]["model"] = self.action_agent_model.get()
        config["action_agent"]["temperature"] = self.temperature_var.get()

        config["curriculum_agent"]["model"] = self.curriculum_agent_model.get()
        config["curriculum_agent"]["temperature"] = self.temperature_var.get()
        config["curriculum_agent"]["qa_model"] = self.curriculum_qa_model.get()
        config["curriculum_agent"]["qa_temperature"] = self.temperature_var.get()

        config["critic_agent"]["model"] = self.critic_agent_model.get()
        config["critic_agent"]["temperature"] = self.temperature_var.get()

        config["skill_manager"]["model"] = self.skill_manager_model.get()
        config["skill_manager"]["temperature"] = self.temperature_var.get()

        config["reasoning_effort"] = self.reasoning_effort.get()
        config["verbosity"] = self.verbosity.get()
        config["store"] = self.store.get()

        return config

    def _save_config(self):
        """Save configuration to JSON file."""
        config = self._get_config_from_ui()
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Voyager Configuration",
        )
        if filename:
            try:
                with open(filename, "w") as f:
                    json.dump(config, f, indent=4)
                messagebox.showinfo("Success", f"Configuration saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save configuration: {e}")

    def _load_config(self):
        """Load configuration from JSON file."""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Load Voyager Configuration",
        )
        if filename:
            try:
                with open(filename, "r") as f:
                    config = json.load(f)

                self.config = config
                self._update_ui_from_config()
                messagebox.showinfo("Success", f"Configuration loaded from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load configuration: {e}")

    def _update_ui_from_config(self):
        """Update UI elements from loaded configuration."""
        self.action_agent_model.set(self.config["action_agent"]["model"])
        self.curriculum_agent_model.set(self.config["curriculum_agent"]["model"])
        self.curriculum_qa_model.set(self.config["curriculum_agent"]["qa_model"])
        self.critic_agent_model.set(self.config["critic_agent"]["model"])
        self.skill_manager_model.set(self.config["skill_manager"]["model"])

        self.reasoning_effort.set(self.config.get("reasoning_effort", "none"))
        self.verbosity.set(self.config.get("verbosity", "medium"))
        self.store.set(self.config.get("store", "false"))

        temp = self.config["action_agent"].get("temperature", 0.0)
        self.temperature_var.set(temp)
        self.temperature_label.configure(text=f"{temp:.1f}")

    def _generate_code(self):
        """Generate Python code with the selected configuration."""
        config = self._get_config_from_ui()

        code = '''"""Voyager configuration generated by GUI.

Alternatively, you can save a JSON config and use example_usage.py to load it:
    from example_usage import load_voyager_from_config
    voyager, options = load_voyager_from_config("your_config.json")
    voyager.learn()
"""
import os
from voyager import Voyager

# Set your OpenAI API key
openai_api_key = "YOUR_OPENAI_API_KEY"

# Azure login configuration (recommended)
azure_login = {
    "client_id": "YOUR_CLIENT_ID",
    "redirect_url": "https://127.0.0.1/auth-response",
    "secret_value": "[OPTIONAL] YOUR_SECRET_VALUE",
    "version": "fabric-loader-0.14.18-1.19",
}

# Initialize Voyager with configured models
voyager = Voyager(
    azure_login=azure_login,
    openai_api_key=openai_api_key,
    action_agent_model_name="{action_model}",
    action_agent_temperature={action_temp},
    curriculum_agent_model_name="{curriculum_model}",
    curriculum_agent_temperature={curriculum_temp},
    curriculum_agent_qa_model_name="{qa_model}",
    curriculum_agent_qa_temperature={qa_temp},
    critic_agent_model_name="{critic_model}",
    critic_agent_temperature={critic_temp},
    skill_manager_model_name="{skill_model}",
    skill_manager_temperature={skill_temp},
)

# Additional Chat Completions API options
# These can be passed as model_kwargs to LangChain's ChatOpenAI
chat_completions_options = {{
    "reasoning_effort": "{reasoning_effort}",
    "verbosity": "{verbosity}",
    "store": {store},
}}

# Start lifelong learning
# voyager.learn()
'''.format(
            action_model=config["action_agent"]["model"],
            action_temp=config["action_agent"]["temperature"],
            curriculum_model=config["curriculum_agent"]["model"],
            curriculum_temp=config["curriculum_agent"]["temperature"],
            qa_model=config["curriculum_agent"]["qa_model"],
            qa_temp=config["curriculum_agent"]["qa_temperature"],
            critic_model=config["critic_agent"]["model"],
            critic_temp=config["critic_agent"]["temperature"],
            skill_model=config["skill_manager"]["model"],
            skill_temp=config["skill_manager"]["temperature"],
            reasoning_effort=config["reasoning_effort"],
            verbosity=config["verbosity"],
            store=config["store"].lower() == "true",
        )

        filename = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")],
            title="Save Generated Python Code",
        )
        if filename:
            try:
                with open(filename, "w") as f:
                    f.write(code)
                messagebox.showinfo("Success", f"Code generated and saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save code: {e}")

    def _reset(self):
        """Reset configuration to defaults."""
        self.config = self._create_default_config()
        self._update_ui_from_config()
        messagebox.showinfo("Reset", "Configuration reset to defaults")


def main():
    """Main entry point."""
    root = tk.Tk()
    app = VoyagerConfigGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
