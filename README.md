# QuestForge

Minecraft Java Edition 1.20.1 Forge modpack focused on survival progression, exploration, building, automation, technology, NPC/AI mechanics and a real FTB Quests progression book.

## Locked platform

- Minecraft: **1.20.1**
- Loader: **Forge 47.4.23**
- Java: **17 x64**
- Pack manager: **packwiz**
- Repository: **Maximka10/questforge**

Minecraft 1.20.1 is used because it has a mature Forge ecosystem. Forge 47.4.23 is the current 1.20.1 release at project creation time. Java 17 is required for the 1.20.1 Forge toolchain.

## Design

QuestForge is intentionally not a kitchen sink. The core loop is:

`survival → exploration → base → storage → Create automation → Mekanism progression → magic → dangerous structures → MineColonies → advanced automation → endgame projects`

The pack uses FTB Quests as the progression layer. Quest data is kept in the repository so the book is part of the project, not an afterthought.

## What the build produces

The build workflow produces a **ready `.minecraft` tree**, including:

```text
QuestForge-ready/
├── versions/1.20.1-forge-47.4.23/
├── mods/
├── config/
├── defaultconfigs/
├── kubejs/
├── resourcepacks/
├── shaderpacks/
└── INSTALL.txt
```

The `versions/1.20.1-forge-47.4.23` directory is intended to be copied to `.minecraft/versions/`. The other directories go beside it in `.minecraft`.

The official Minecraft launcher may download missing vanilla libraries/assets on first launch. That is normal; those files are not distributed by this repository.

## AI / NPC

The stable NPC layer is **MineColonies**. Citizens have jobs and builders can construct structures, making NPCs a real part of progression rather than a cosmetic addition.

An experimental AI-Buddies profile is documented separately. It is not included in the stable package until it passes a clean Forge 1.20.1 startup and gameplay validation.

## Quest Book

The generated book contains 10 progression chapters and 40 quests covering onboarding, exploration, building, storage, technology, magic, combat, colonies, advanced automation and endgame. Dependencies connect the chapters into a progression path.

## Installation on Windows

1. Install 64-bit Java 17.
2. Download the `QuestForge-1.20.1-Forge-47.4.23-ready.zip` artifact from the latest successful GitHub Actions build.
3. Extract it.
4. Copy the contents of `drop-in/` into `%APPDATA%\\.minecraft`.
5. Launch the Forge 1.20.1-47.4.23 profile.
6. Start a new world for the first validation run.

## Troubleshooting

### If Minecraft does not launch

1. Verify Java is version 17 and 64-bit.
2. Verify the selected profile is Forge 47.4.23 on Minecraft 1.20.1.
3. Check `.minecraft/logs/latest.log`.
4. Find the first `Caused by:` block rather than only the last crash line.
5. If a dependency is missing, rebuild from this repository so packwiz regenerates the locked dependency graph.
6. Do not mix jars from another modpack into the QuestForge `mods` directory.

## Server

See `docs/server.md`. Client-only mods must not be copied to a dedicated server manually.

## Development

`scripts\\bootstrap.ps1` initializes the pack and resolves the manifest. `scripts\\generate_quests.py` generates the Quest Book. `scripts\\build.ps1` refreshes the pack and exports it. GitHub Actions is the authoritative clean-build validation.
