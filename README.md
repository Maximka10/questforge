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

QuestForge is intentionally not a 300-mod kitchen sink. The core loop is:

`survival → exploration → base → storage → Create automation → Mekanism progression → magic → dangerous structures → MineColonies → advanced automation → endgame projects`

The pack uses FTB Quests as the progression layer. Quest data is kept in the repository so the book is part of the project, not an afterthought.

## AI / NPC

The pack treats NPC automation as a first-class gameplay system through MineColonies. An experimental profile for **AI-Buddies** is documented separately. AI-Buddies is a Forge 1.20.1 mod with local/simple chat-command companions and no third-party API key requirement, but it has a much smaller adoption footprint than the core pack, so it is not part of the default profile until it passes the same startup and gameplay checks as the core pack.

## Repository layout

```text
config/                 Shared configuration
defaultconfigs/         Default server configs
kubejs/                 Recipes and balance scripts
quests/                 Quest Book source/data
scripts/                Bootstrap/build/diagnostic scripts
server/                 Dedicated-server helpers
packwiz/                Pack metadata and generated mod metadata
.github/workflows/      Automated build validation
docs/                   Design and compatibility notes
```

## First setup on Windows

1. Install 64-bit Java 17.
2. Clone this repository.
3. Run `scripts\\bootstrap.ps1` from PowerShell.
4. The script downloads packwiz if needed, initializes the pack metadata and installs the pinned mod set defined in `scripts\\mods.txt`.
5. Run `scripts\\build.ps1` to refresh the index and create a distributable `.mrpack`.

The first bootstrap requires internet access because mod binaries are deliberately not committed to Git.

## Updating

Do not blindly run `packwiz update --all`. Review updates in a branch, run the validation workflow, launch a clean client and create a new world before merging.

## Server

The same pack metadata can be used for a dedicated Forge server. Client-only mods must stay client-only. Server setup is documented in `docs/server.md` and automated by `scripts\\server.ps1`.

## Troubleshooting

### If Minecraft does not launch

1. Verify that Java reports version 17 and is 64-bit.
2. Verify Forge is 47.4.23.
3. Delete the generated `mods` cache only if the bootstrap reports a corrupted download.
4. Run `scripts\\diagnose.ps1`.
5. Check `logs\\latest.log` and search for the first `Caused by:` block, not just the final crash line.
6. If the error names a dependency, rerun bootstrap so packwiz can resolve the dependency graph.
7. If the error is caused by a mod update, restore the last known-good commit rather than mixing arbitrary versions.

## Status

The repository is being built as a reproducible packwiz project. The mod list, quest structure and automation are version-controlled; the CI workflow is the authoritative clean-build check.
