# Vanilla Minecraft Compatibility

## Overview

Voyager now works with **vanilla Minecraft** (any Java Edition version) without requiring any mods or mod loaders!

## Key Features

✅ **No mods required** - Works perfectly with vanilla Minecraft  
✅ **No mod loader required** - No need to install Fabric, Forge, or any other mod loader  
✅ **Any Minecraft version** - Compatible with most Minecraft Java Edition versions  
✅ **Simple setup** - Just install Minecraft, open a world to LAN, and start learning  
✅ **Lower barrier to entry** - Get started immediately without complex configuration

## Quick Start

1. **Install Voyager** (Python + Node.js packages)
   ```bash
   pip install -e .
   cd voyager/env/mineflayer && npm install
   ```

2. **Launch vanilla Minecraft**
   - Any version (recommended: 1.16.5 or later)
   - Create or open a world
   - Set to Creative mode, Peaceful difficulty

3. **Open to LAN**
   - Press `Esc` → `Open to LAN`
   - Enable cheats: ON
   - Start LAN World
   - Note the port number

4. **Run Voyager**
   ```python
   from voyager import Voyager
   
   voyager = Voyager(
       mc_port=25565,  # Your port from step 3
       openai_api_key="YOUR_KEY"
   )
   
   voyager.learn()
   ```

## Supported Versions

| Version Range | Status | Notes |
|--------------|--------|-------|
| 1.16.5 - 1.19.x | ✅ Recommended | Most extensively tested |
| 1.12.2 - 1.15.x | ✅ Compatible | Should work well |
| 1.8 - 1.11.x | ⚠️ Limited | May have compatibility issues |
| Latest (1.20+) | ✅ Should Work | Mineflayer generally supports new versions |

## What About Mods?

Mods are now **completely optional**. They only provide quality-of-life improvements:

### Without Mods (Vanilla)
- ✅ Core functionality works perfectly
- ✅ LLM-driven learning and skill acquisition
- ✅ All Minecraft interactions
- ⏱️ Time continues during GPT API calls

### With Optional Mods
- ✅ Everything vanilla has
- ⏸️ Game pauses during GPT API calls
- 🎮 Enhanced respawn control
- 📋 Mod management UI

**Recommendation**: Start with vanilla, add mods later if needed.

## Benefits of Vanilla Support

1. **Simpler Installation**
   - No mod loader configuration
   - No compatibility checks between mods
   - No mod version matching

2. **Wider Compatibility**
   - Works with any Minecraft version you own
   - No version-specific mod requirements
   - Easier to update Minecraft

3. **Faster Setup**
   - Install and run in minutes
   - No mod compilation or configuration
   - Fewer things that can go wrong

4. **Better for Beginners**
   - Standard Minecraft installation
   - Familiar launcher interface
   - Easy to troubleshoot

## Technical Details

### How It Works

Voyager uses **mineflayer**, a Node.js library that:
- Connects to Minecraft via the standard protocol
- Works with vanilla servers (including LAN worlds)
- Supports multiple Minecraft versions
- Requires no server-side modifications

### What's Different?

**Old approach (Azure + Fabric):**
```
Azure AD → minecraft_launcher_lib → Fabric loader → Mods → Minecraft
```

**New approach (Vanilla):**
```
Minecraft Official Launcher → LAN World → mineflayer → Voyager
```

## Migration from Modded Setup

If you were using Voyager with Fabric mods:

1. **Vanilla mode works immediately** - just skip mod installation
2. **Your skills library is compatible** - works with or without mods
3. **Same API, same code** - no changes to your Voyager scripts
4. **You can still use mods** - they're optional, not removed

## Troubleshooting

### "Bot won't connect"
- Verify Minecraft world is open to LAN
- Check you're using the correct port number
- Ensure "Allow cheats" is ON

### "Incompatible version"
- Try Minecraft 1.16.5 - 1.19.x (best tested)
- Update mineflayer: `cd voyager/env/mineflayer && npm update`

### "Missing mods error"
- You don't need mods! This shouldn't happen with vanilla
- If you see this, you may have old Fabric configs

## FAQ

**Q: Do I need Fabric?**  
A: No, Fabric is completely optional.

**Q: What Minecraft version should I use?**  
A: Any version works, but 1.16.5-1.19.x is recommended.

**Q: Can I still use mods?**  
A: Yes! Mods are optional. See [Optional Mods Guide](installation/fabric_mods_install.md).

**Q: Will my existing skill libraries work?**  
A: Yes, skill libraries are version-independent and work with or without mods.

**Q: What if I'm on the latest Minecraft version?**  
A: It should work! Mineflayer typically supports new versions quickly.

## Learn More

- [Main README](README.md) - Full documentation
- [Minecraft Setup Guide](installation/minecraft_instance_install.md) - Detailed setup
- [Optional Mods](installation/fabric_mods_install.md) - If you want mods
- [FAQ](FAQ.md) - Common questions

---

**Ready to get started?** Jump straight to the [Getting Started](README.md#getting-started) section!
