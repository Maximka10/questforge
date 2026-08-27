# AI / NPC companion decision

## Default

The default pack uses **MineColonies** as the stable NPC/automation layer. Its citizens can be assigned jobs, builders can construct structures, and the colony creates a persistent population that participates in the player's long-term base progression.

This is deliberately different from claiming that the NPCs are a conversational LLM agent.

## Experimental AI-Buddies

AI-Buddies is a Forge 1.20.1 mod advertised as providing 1-6 AI companions with simple chat commands and no API keys. It has a much smaller adoption footprint than the core QuestForge mods, so it is kept out of the default profile until a clean 1.20.1 Forge 47.4.x startup test and a basic companion gameplay test pass.

To trial it locally, uncomment `cf|ai-buddies` in `scripts/mods.txt`, run bootstrap again, then verify:

1. Client starts without dependency or mixin errors.
2. A new world loads.
3. A companion can be spawned.
4. Follow/command behavior works.
5. The companion does not corrupt saves or cause persistent tick lag.

If any of those fail, leave the mod disabled. Do not add an external API key to Git.
