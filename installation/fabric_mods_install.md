# Optional Mods for Enhanced Experience

**Note**: Mods are **completely optional**. Voyager works perfectly with vanilla Minecraft without any mods or mod loaders. The mods described here only provide quality-of-life improvements and are not required for core functionality.

## Why Use Mods?

While Voyager works great with vanilla Minecraft, these optional mods can enhance the experience:

- **Server Pause**: Pauses the game world while waiting for GPT-4 responses (prevents time-sensitive issues)
- **Better Respawn**: Provides more control over respawn behavior (useful for certain tasks)
- **Mod Menu**: Makes it easier to manage mods if you choose to use them

## Should You Install Mods?

Choose **vanilla Minecraft** (no mods) if:
- ✅ You want the simplest setup
- ✅ You're just getting started with Voyager
- ✅ You want maximum version compatibility
- ✅ You don't want to deal with mod installation

Choose **modded Minecraft** (optional) if:
- ⚡ You want the game to pause during GPT-4 API calls
- ⚡ You want enhanced control over game mechanics
- ⚡ You don't mind a more complex setup

## Installing Mods (Optional)

If you decide to use mods, here's how to install them for Minecraft 1.19:

### 1. Install Fabric Loader

Download and install the Fabric Loader from [fabricmc.net](https://fabricmc.net/use/installer/):
- **Windows**: Download the `.exe` installer
- **Mac/Linux**: Download the `.jar` file and run `java -jar fabric-installer-0.11.2.jar`
- Select game version: `1.19`
- Select loader version: `0.14.18`

After installation, you'll have:
- A `mods` folder in your Minecraft directory
- A new Minecraft version: `fabric-loader-0.14.18-1.19`

### 2. Download Optional Mods

Place these mods in the `mods` folder:

#### Essential Mods:
- **[Fabric API](https://modrinth.com/mod/fabric-api/version/0.58.0+1.19)** - Required for other mods to work
- **[Mod Menu](https://cdn.modrinth.com/data/mOgUt4GM/versions/4.0.4/modmenu-4.0.4.jar)** - Manages installed mods

#### Quality-of-Life Mods:
- **[Complete Config](https://www.curseforge.com/minecraft/mc-mods/completeconfig/download/3821056)** - Dependency for server pause
- **[Multi Server Pause](https://www.curseforge.com/minecraft/mc-mods/multiplayer-server-pause-fabric/download/3822586)** - Pauses during GPT-4 calls

#### Advanced Mods:
- **[Better Respawn](https://github.com/xieleo5/better-respawn/tree/1.19)** - Enhanced respawn control (requires manual compilation)

### 3. Configure Better Respawn (if using)

To compile Better Respawn:
```bash
git clone https://github.com/xieleo5/better-respawn
cd better-respawn
# Remove 'forge' from the last line of settings.gradle
gradlew build
# Copy: fabric/build/libs/better-respawn-fabric-1.19-2.0.0.jar to mods folder
```

Then configure it at `YOUR_MINECRAFT_DIR/config/better-respawn/properties`:
```
respawn_block_range=32
max_respawn_distance=32
min_respawn_distance=0
```

**Note**: You need Java 17+ to build Better Respawn. Get it from [Oracle's website](https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html).

### 4. Launch with Fabric

In the Minecraft launcher:
- Select the `fabric-loader-0.14.18-1.19` profile
- Launch and play as normal

## Other Minecraft Versions

The mods listed above are for Minecraft 1.19. If you're using a different version:
- Find mods compatible with your specific version
- Look for the same mod names on [Modrinth](https://modrinth.com) or [CurseForge](https://www.curseforge.com/minecraft)
- Many mods support multiple Minecraft versions

## Troubleshooting Mods

If you have issues with mods:
1. **Try vanilla Minecraft first** - verify Voyager works without mods
2. Check mod compatibility with your Minecraft version
3. Ensure Fabric API is installed (required by most mods)
4. Check the Minecraft log for error messages

## Recommendation

For most users, we recommend **starting with vanilla Minecraft** to ensure everything works, then optionally adding mods later if desired.

---

Return to [README.md](../README.md#getting-started) to continue setup.
