# Progression

How the pack should grow, and how a player should be led through it. **PLANNED, NOT YET
BUILT.** Nothing in this file is implemented; it records the direction so it is not lost.
Written 2026-10-19 from an outside suggestion, with the decisions below layered on top.

## The rule

Stages describe what kinds of play the pack offers, not a locked sequence. Players specialise
and trade. Progression makes the relationships between mods legible and stops accidental
skips; it does not dictate one way to play.

## Stages

| Stage | What it is | In the pack today | Note |
|---|---|---|---|
| 1 Fieldcraft | stone and copper tools, exploring, gathering, farming, first settlements | Copper Tools, Farmer's Delight, Terralith | already playable |
| 2 Metallurgy | iron, steel, deliberate processing | Oritech, Oritech Steel Tools | steel should NEED Oritech processing, or stage 3 has no hook |
| 3 Industrialization | power, machines, logistics, automation | Oritech power and machines | gap: no item transport mod yet |
| 4 Specialised mastery | intentional enchanting, rare ingredients, advanced gear | Modest Magic, More Delight | magic and tech trade ingredients; neither replaces the other |
| 5 Infrastructure | shared factories, transport, community projects | nothing | needs a population. Designed after launch, not before |

Each system earns its place: copper fills stone-to-iron, steel rewards processing, Modest
Magic makes enchanting a choice. Food: farming gives ingredients, cooking gives
specialisation, automation is optional scale. Not every meal is a factory part.

## The guide: an FTB-style quest book

Decided: the guide is a quest book in the FTB Quests mould. Chapters per stage, a quest map,
item-submission and checkmark tasks, rewards, and descriptions that say why the next mod
matters. **Which mod is OPEN**, the owner is researching it.

The choice has to meet these, so a candidate can be checked against them:

- a Fabric 1.21.1 build now, and a path to 26.x later
- installable through packwiz: Modrinth, or CurseForge with third-party distribution allowed
  (packwiz-installer cannot fetch CurseForge files that block it)
- quest data as text files that live in this repo and review as diffs, not a binary blob
- works on a dedicated server

Known so far:

- **FTB Quests** is CurseForge only. Its addons are on Modrinth for Fabric 1.21.1, so the
  mod itself exists there.
- **Odyssey Quests** is on Modrinth, tree-style and maintained.

Advancements stay useful either way: they are the fallback guide, and wly already posts them
to the Discord feed with a map of where they happened.

## Connecting mods: datapacks, not KubeJS

KubeJS has no Fabric build for 1.21.1 or 26.x. Recipes that make one mod lead into the next
are datapack recipe overrides plus tags. Anything a datapack cannot express goes into a small
Kotlin mod of our own.

**Verify before the first datapack ships:** how a datapack reaches the server's EXISTING
world. Global Packs loads its datapack folders when a world is created, and the live world is
old. Likely `world/datapacks/` or itzg's `DATAPACKS` setting.

## Road to launch

1. **Now, friends only:** finish the look (panorama, FancyMenu layout), fix the leaf piles,
   find a Fog replacement.
2. **Stages 1 to 3 legible:** pick the quest mod and write the stage 1 to 3 chapters, steel
   gated on Oritech, item transport.
3. **Stage 4:** Modest Magic and the cooking mods tied in with cross-ingredients.
4. **Launch readiness:** a domain, port 25565 opened on purpose (the whitelist is really on
   now), the off-box backup target set, view distance checked against real load. These live
   in weloveyou.mc's CLAUDE.md.
5. **Launch.** Stage 5 is designed once there are players to build it for.

## Avoid

- a linear quest chain that locks content: chapters guide, they do not gate
- gating vanilla basics: people leave a pack that hides iron
- building stage 5 economy features before anyone is there to use them
