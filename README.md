# Voyager: An Open-Ended Embodied Agent with Large Language Models
<div align="center">

[[Website]](https://voyager.minedojo.org/)
[[Arxiv]](https://arxiv.org/abs/2305.16291)
[[PDF]](https://voyager.minedojo.org/assets/documents/voyager.pdf)
[[Tweet]](https://twitter.com/DrJimFan/status/1662115266933972993?s=20)

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://github.com/MineDojo/Voyager)
[![Node Version](https://img.shields.io/badge/Node.js-18.20.8%2B-green.svg)](https://github.com/MineDojo/Voyager)
[![GitHub license](https://img.shields.io/github/license/MineDojo/Voyager)](https://github.com/MineDojo/Voyager/blob/main/LICENSE)
______________________________________________________________________


https://github.com/MineDojo/Voyager/assets/25460983/ce29f45b-43a5-4399-8fd8-5dd105fd64f2

![](images/pull.png)


</div>

We introduce Voyager, the first LLM-powered embodied lifelong learning agent
in Minecraft that continuously explores the world, acquires diverse skills, and
makes novel discoveries without human intervention. Voyager consists of three
key components: 1) an automatic curriculum that maximizes exploration, 2) an
ever-growing skill library of executable code for storing and retrieving complex
behaviors, and 3) a new iterative prompting mechanism that incorporates environment
feedback, execution errors, and self-verification for program improvement.
Voyager interacts with GPT-4 via blackbox queries, which bypasses the need for
model parameter fine-tuning. The skills developed by Voyager are temporally
extended, interpretable, and compositional, which compounds the agent’s abilities
rapidly and alleviates catastrophic forgetting. Empirically, Voyager shows
strong in-context lifelong learning capability and exhibits exceptional proficiency
in playing Minecraft. It obtains 3.3× more unique items, travels 2.3× longer
distances, and unlocks key tech tree milestones up to 15.3× faster than prior SOTA.
Voyager is able to utilize the learned skill library in a new Minecraft world to
solve novel tasks from scratch, while other techniques struggle to generalize.

In this repo, we provide Voyager code. This codebase is under [MIT License](LICENSE).

> **🎮 New: Vanilla Minecraft Support!**  
> Voyager now works with any version of vanilla Minecraft - no mods or mod loaders required!  
> See [Vanilla Minecraft Guide](VANILLA_MINECRAFT.md) for a quick start.

# Installation
Voyager requires Python ≥ 3.9 (compatible with Python 3.14) and Node.js ≥ 18.20.8 (compatible with Node.js 25 and LTS versions). It works with **any version of vanilla Minecraft** (no mods or mod loaders required). We have tested on Ubuntu 20.04, Windows 11, and macOS. You need to follow the instructions below to install Voyager.

## Python Install
```
git clone https://github.com/MineDojo/Voyager
cd Voyager
pip install -e .
```

## Node.js Install
In addition to the Python dependencies, you need to install the following Node.js packages:
```
cd voyager/env/mineflayer
npm install -g npx
npm install
cd mineflayer-collectblock
npm install
npx tsc
cd ..
npm install
```
(You can safely ignore messages like [npm warn deprecated ...] and [5 high severity vulnerabilities] )

## Minecraft Setup

Voyager works with vanilla Minecraft (any version). You just need to have Minecraft installed on your system. No mods or mod loaders are required.

For detailed setup instructions, see [Minecraft Setup Guide](installation/minecraft_instance_install.md).

**Note**: While Voyager works with any Minecraft version, some optional quality-of-life features may require mods (see [Optional Mods](installation/fabric_mods_install.md) for details). However, the core functionality works perfectly with vanilla Minecraft.

# GUI Configuration Tool

Voyager includes a GUI tool (`gui.py`) to help you configure agent models and supported API parameters without editing code.

The GUI uses **PyQt6**.

## Using the GUI

Launch the configuration tool:

```bash
python gui.py
```

The GUI provides these tabs:

### Models
Select which GPT model to use for each agent.

### Settings (new)
Configure modern options:
- `reasoning_effort`
- `verbosity`
- `store`

### Old settings (legacy)
Configure legacy options:
- `temperature`
- `max_tokens`
- `top_p`
- `store`

The **Old settings** tab is only available when all selected agent models are within the legacy range `gpt-3.5-turbo` .. `gpt-4.1`.

For detailed documentation, see [GUI_README.md](GUI_README.md).

## Using Generated Configuration

After generating a Python script with the "Generate Code" button, you can:
1. Edit the file to add your OpenAI API key and Minecraft port
2. Run the script to start Voyager with your chosen configuration

# Getting Started
Voyager uses OpenAI's GPT-4 as the language model. You need to have an OpenAI API key to use Voyager. You can get one from [here](https://platform.openai.com/account/api-keys).

After the installation process, you need to:
1. Start Minecraft and create a world
2. Set Game Mode to `Creative` and Difficulty to `Peaceful`
3. Press `Esc` and select `Open to LAN`
4. Enable `Allow cheats: ON` and press `Start LAN World`
5. Note the port number shown in the chat (e.g., 25565)

Then you can run Voyager by:
```python
from voyager import Voyager

# Replace with your actual Minecraft port from step 5 above
mc_port = 25565
openai_api_key = "YOUR_API_KEY"

voyager = Voyager(
    mc_port=mc_port,
    openai_api_key=openai_api_key,
)

# start lifelong learning
voyager.learn()
``` 

# Resume from a checkpoint during learning

If you stop the learning process and want to resume from a checkpoint later, you can instantiate Voyager by:
```python
from voyager import Voyager

voyager = Voyager(
    mc_port=mc_port,
    openai_api_key=openai_api_key,
    ckpt_dir="YOUR_CKPT_DIR",
    resume=True,
)
```

# Run Voyager for a specific task with a learned skill library

If you want to run Voyager for a specific task with a learned skill library, you should first pass the skill library directory to Voyager:
```python
from voyager import Voyager

# First instantiate Voyager with skill_library_dir.
voyager = Voyager(
    mc_port=mc_port,
    openai_api_key=openai_api_key,
    skill_library_dir="./skill_library/trial1", # Load a learned skill library.
    ckpt_dir="YOUR_CKPT_DIR", # Feel free to use a new dir. Do not use the same dir as skill library because new events will still be recorded to ckpt_dir. 
    resume=False, # Do not resume from a skill library because this is not learning.
)
```
Then, you can run task decomposition. Notice: Occasionally, the task decomposition may not be logical. If you notice the printed sub-goals are flawed, you can rerun the decomposition.
```python
# Run task decomposition
task = "YOUR TASK" # e.g. "Craft a diamond pickaxe"
sub_goals = voyager.decompose_task(task=task)
```
Finally, you can run the sub-goals with the learned skill library:
```python
voyager.inference(sub_goals=sub_goals)
```

For all valid skill libraries, see [Learned Skill Libraries](skill_library/README.md).

# FAQ
If you have any questions, please check our [FAQ](FAQ.md) first before opening an issue.

# Paper and Citation

If you find our work useful, please consider citing us! 

```bibtex
@article{wang2023voyager,
  title   = {Voyager: An Open-Ended Embodied Agent with Large Language Models},
  author  = {Guanzhi Wang and Yuqi Xie and Yunfan Jiang and Ajay Mandlekar and Chaowei Xiao and Yuke Zhu and Linxi Fan and Anima Anandkumar},
  year    = {2023},
  journal = {arXiv preprint arXiv: Arxiv-2305.16291}
}
```

Disclaimer: This project is strictly for research purposes, and not an official product from NVIDIA.
