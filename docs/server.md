# Dedicated server

QuestForge uses Forge 47.4.23 on Minecraft 1.20.1. Keep Java 17 x64 on the server.

## Installation model

The repository does not commit Minecraft or mod binaries. Build the pack first with `scripts\bootstrap.ps1` and `scripts\build.ps1`, then install the resulting pack on the server with a packwiz installer or export the server-compatible files.

For a hosted server, point packwiz-installer at the hosted `pack.toml` and use the server side flag so client-only mods are excluded.

```text
java -jar packwiz-installer-bootstrap.jar -g -s server https://YOUR-HOST/pack.toml
```

Accept the Minecraft EULA in the server directory before starting the dedicated server.

## Client/server split

The authoritative source is each generated `.pw.toml` file. Do not manually copy client-only visual mods to the server. MineColonies, Create, Mekanism, FTB Quests and the world-generation mods are intended to participate in the common/server profile.

## First boot

1. Install Java 17 x64.
2. Install the server pack.
3. Accept `eula=true`.
4. Start once and stop after the first clean generation.
5. Review `logs/latest.log` for `ERROR`, `FATAL` and dependency failures.
6. Only then create the production world.
