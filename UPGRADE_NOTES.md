# Upgrade Notes: Python 3.14, Node.js 25, OpenAI-Only, Vanilla Minecraft

This document summarizes the changes made to upgrade the repository for Python 3.14, Node.js 25 compatibility, removal of Azure dependencies, and vanilla Minecraft support (no mods required).

## Python 3.14 Compatibility

### Changes Made:
- Updated `setup.py` to include Python 3.10, 3.11, 3.12, 3.13, and 3.14 in classifiers
- Python version requirement remains `>=3.9` to maintain backward compatibility
- All code is compatible with Python 3.14 (no deprecated features used)

## Node.js 25 and LTS Compatibility

### Changes Made:
- Added `engines` field to `voyager/env/mineflayer/package.json`
- Specified Node.js version requirement: `>=18.20.8`
- This ensures compatibility with Node.js 25 and current LTS versions
- Updated README badge to show Node.js compatibility

## Azure Dependencies Removal

### Files Modified:

1. **voyager/env/bridge.py**
   - Removed `azure_login` parameter from `VoyagerEnv.__init__()`
   - Made `mc_port` a required parameter (no longer optional)
   - Removed `get_mc_instance()` method
   - Removed Azure-related imports (`MinecraftInstance`)
   - Removed logic to start/manage Minecraft instances via Azure

2. **voyager/voyager.py**
   - Removed `azure_login` parameter from `Voyager.__init__()`
   - Made `mc_port` a required parameter
   - Updated docstring to reflect mc_port is required

3. **example_usage.py**
   - Replaced `azure_login` parameter with `mc_port`
   - Updated prompts to ask for mc_port instead of Azure credentials
   - Added instructions for obtaining the port

4. **voyager_config_example.py**
   - Replaced Azure login configuration with mc_port
   - Added detailed instructions on how to obtain the port

5. **gui.py**
   - Updated code generation to use `mc_port` instead of `azure_login`
   - Added instructions in generated code for obtaining the port

6. **requirements.txt**
   - Removed `minecraft_launcher_lib` dependency (was used for Azure authentication)

7. **README.md**
   - Updated installation instructions
   - Removed Azure login references
   - Added clear steps for using Minecraft Official Launcher
   - Updated version badges to show Python 3.9+ and Node.js 18.20.8+
   - Updated all code examples to use `mc_port`

8. **FAQ.md**
   - Removed all Azure-related FAQ entries
   - Kept only relevant questions
   - Updated code examples to use `mc_port`

9. **installation/minecraft_instance_install.md**
   - Removed Azure login section entirely
   - Kept only Minecraft Official Launcher instructions
   - Added clear code example

10. **installation/fabric_mods_install.md**
    - Removed Azure-related notes
    - Cleaned up formatting

### Files Removed:
- **voyager/env/minecraft_launcher.py** - This file handled Azure authentication and Minecraft instance launching

## Migration Guide for Users

### Before (with Azure):
```python
from voyager import Voyager

azure_login = {
    "client_id": "YOUR_CLIENT_ID",
    "redirect_url": "https://127.0.0.1/auth-response",
    "secret_value": "YOUR_SECRET_VALUE",
    "version": "fabric-loader-0.14.18-1.19",
}

voyager = Voyager(
    azure_login=azure_login,
    openai_api_key="YOUR_API_KEY",
)
```

### After (OpenAI-only):
```python
from voyager import Voyager

# Steps to get mc_port:
# 1. Start Minecraft and create a world
# 2. Set Game Mode to Creative and Difficulty to Peaceful
# 3. Press Esc and select "Open to LAN"
# 4. Enable "Allow cheats: ON" and press "Start LAN World"
# 5. Note the port number from the chat (e.g., 25565)

mc_port = 25565  # Replace with your actual port

voyager = Voyager(
    mc_port=mc_port,
    openai_api_key="YOUR_API_KEY",
)
```

## Vanilla Minecraft Support

### Changes Made:
- **No mods required**: Voyager now works with any version of vanilla Minecraft Java Edition
- **No mod loader required**: Fabric and other mod loaders are completely optional
- Updated all documentation to emphasize vanilla compatibility
- Made mod installation instructions optional (quality-of-life improvements only)
- Removed hard dependencies on specific Minecraft versions

### Supported Minecraft Versions:
- **Recommended**: 1.16.5 - 1.19.x (most tested)
- **Compatible**: 1.12.2 and later (should work well)
- **Older**: 1.8 - 1.11.x (may have limited compatibility)

### Optional Mods:
Mods are now completely optional. They provide quality-of-life features like:
- Server pause during GPT-4 API calls
- Enhanced respawn control
- But they are **not required** for Voyager to function

## Benefits of These Changes

1. **Simpler Setup**: No need to configure Azure Active Directory apps
2. **Fewer Dependencies**: Removed `minecraft_launcher_lib` dependency
3. **More Maintainable**: Less complexity in the codebase
4. **Better Compatibility**: Support for latest Python and Node.js versions
5. **Clearer Documentation**: Single, straightforward setup path
6. **Version Flexibility**: Works with any Minecraft version without mods
7. **Lower Barrier to Entry**: Users can start with vanilla Minecraft immediately

## Testing Recommendations

After upgrading, test the following:
1. Python import: `python3 -c "from voyager import Voyager"`
2. Node.js dependencies: `cd voyager/env/mineflayer && npm install`
3. Create a Voyager instance with a valid mc_port
4. Run a simple task to verify functionality
