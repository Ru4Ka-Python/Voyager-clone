# Minecraft Instance Install

To start using Voyager, you should first make sure to have an official [Minecraft](https://www.minecraft.net/) game (version 1.19) installed.

## Minecraft Official Launcher

After you install official Minecraft, you should have a Minecraft official launcher. Open it and follow the instructions here:

1. Select the version you want to play and start the game.
2. Select `Singleplayer` and create a new world.
3. Set Game Mode to `Creative` and Difficulty to `Peaceful`.
4. After the world is created, press `Esc` and select `Open to LAN`.
5. Select `Allow cheats: ON` and press `Start LAN World`.
6. You will see a port number in the chat log, that is your `mc_port`, use this number to instantiate Voyager.

Example:
```python
from voyager import Voyager

# Replace with the port number from step 6
mc_port = 25565

voyager = Voyager(
    mc_port=mc_port,
    openai_api_key="YOUR_OPENAI_API_KEY",
)
```

**Voyager uses `fabric-loader-0.14.18-1.19` version to run all the experiments.** You may not have this version currently. You can move on to the [Fabric Mods Install](fabric_mods_install.md#fabric-mods-install) section and follow the instructions there to install the fabric version of the game.
