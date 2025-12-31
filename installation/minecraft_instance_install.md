# Minecraft Setup Guide

Voyager works with **any version of vanilla Minecraft** - no mods or mod loaders are required!

## Requirements

- Official Minecraft Java Edition (any version)
- The Minecraft Official Launcher

## Setup Instructions

1. **Launch Minecraft**
   - Open the Minecraft launcher
   - Select any version you prefer (recommended: 1.16.5 or later for best compatibility)
   - Click "Play"

2. **Create or Open a World**
   - Select `Singleplayer`
   - Either create a new world or select an existing one
   - **Important**: Set the following settings:
     - Game Mode: `Creative`
     - Difficulty: `Peaceful`

3. **Open World to LAN**
   - Once in the world, press `Esc`
   - Click `Open to LAN`
   - Configure settings:
     - Game Mode: `Creative` (if not already)
     - Allow Cheats: `ON` (required for bot commands)
   - Click `Start LAN World`

4. **Note the Port Number**
   - After starting the LAN world, a message will appear in the chat
   - It will say something like: "Local game hosted on port 25565"
   - **Write down this port number** - you'll need it to connect Voyager

## Using the Port with Voyager

Once you have the port number, use it when creating your Voyager instance:

```python
from voyager import Voyager

# Use the port number from step 4
mc_port = 25565  # Replace with your actual port

voyager = Voyager(
    mc_port=mc_port,
    openai_api_key="YOUR_OPENAI_API_KEY",
)

# Start learning
voyager.learn()
```

## Supported Minecraft Versions

Voyager is designed to work with **any Minecraft Java Edition version**. However:

- **Recommended**: Minecraft 1.16.5 - 1.19.x
  - These versions have been most extensively tested
  - Best compatibility with mineflayer
  
- **Compatible**: Minecraft 1.12.2 and later
  - Should work with minimal issues
  
- **Older Versions**: Minecraft 1.8 - 1.11.x
  - May have limited compatibility
  - Some features might not work as expected

## Troubleshooting

### Port Not Showing
If you don't see a port number in chat:
- Make sure "Allow cheats" was set to ON
- Try restarting the world and opening to LAN again
- Check your game output log

### Connection Issues
If Voyager can't connect:
- Verify the port number is correct
- Make sure the Minecraft world is still running
- Check that no firewall is blocking the connection
- Ensure you're using the correct Minecraft version for your setup

### Bot Not Joining
If the bot doesn't appear in your world:
- Keep the world running and wait a few seconds
- Check the Voyager console output for errors
- Make sure the mineflayer service started correctly (check with `node voyager/env/mineflayer/index.js`)

## Next Steps

After setting up Minecraft:
1. Verify your port number is working
2. Configure Voyager with your OpenAI API key
3. Run your first Voyager session!

For more information, return to [README.md](../README.md#getting-started) to get started.
