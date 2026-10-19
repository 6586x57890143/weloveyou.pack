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
| 1 Fieldcraft | copper tools (no stone), exploring, gathering, farming, first settlements | Copper Tools, Farmer's Delight, Terralith | already playable |
| 2 Metallurgy | iron, steel, deliberate processing | Oritech (Oritech Steel Tools removed in v0.1.17: it broke the enchanting tags) | steel should NEED Oritech processing, or stage 3 has no hook |
| 3 Industrialization | power, machines, logistics, automation | Oritech power and machines | gap: no item transport mod yet |
| 4 Specialised mastery | enchanting by tablet, no levels, rare ingredients, advanced gear | Modest Magic, More Delight | magic and tech trade ingredients; neither replaces the other |
| 5 Infrastructure | shared factories, transport, community projects | nothing | needs a population. Designed after launch, not before |

Each system earns its place: copper fills stone-to-iron, steel rewards processing, Modest
Magic makes enchanting a choice. Food: farming gives ingredients, cooking gives
specialisation, automation is optional scale. Not every meal is a factory part.

## The early game, expanded

Raspberry Flavoured makes the early game longer. We go further: stages 1 and 2 are where the
pack's character lives.

- **The upper layers matter.** Copper, coal, iron and the surface give a reason to mine near
  the top: copper tools, a first dwelling worth building, Farmer's Delight to feed it.
- **Depth is danger.** The deeper you go the more it costs to be careless. Terralith and the
  large caves already do the scary part; the world should keep feeling dangerous and fun, never
  punishing. Not hardcore.
- **Diamonds are a journey, not a lucky dig.** The road there is longer and more dangerous than
  vanilla's. Worldgen datapacks can move or thin diamond ore (ore placement is data driven), so
  the way down is earned.
- **The Oritech goal is amethyst.** Amethyst clusters are the catch for Oritech progression,
  which makes finding a geode a real moment. See the JourneyMap question below: a cave map
  makes that moment cheap.

**Mobs hit harder, in steps.** The server runs `difficulty=easy`, itzg's default, never chosen.
Step one is Normal: in vanilla a hit that does 3 hearts on Normal does 2 on Easy and 4.5 on Hard.
Then, if it still feels soft, a targeted damage boost on top (a mob attribute change in the
small mod), measured against how the caves play, not set once and forgotten.

**Open: JourneyMap.** It is client-only in the pack. The tension is mostly its cave map and
radar, which turn exploring underground into reading a screen, while the surface map is pure
convenience. The preferred shape: surface map in the Overworld only, no cave map, no radar, no
map in the Nether. JourneyMap 6.x has server-side admin controls once it is installed on the
server too (recent builds: disable the minimap, hide coordinates, cap cave render distance).
Whether it can turn the cave map or a whole dimension off is NOT confirmed. Install it
server-side in the dev loop (`scripts/pack-dev.sh play`) and look at its admin screen before
deciding. If it cannot, the choice is keep it whole or drop it.

## Opinionated changes (decided, not built)

Raspberry Flavoured's stance, adopted: changes are deliberate, and luck gives way to choice.

**Copper replaces stone.** Stone tools are not craftable; copper tools (the Copper Tools mod,
already in the pack) are the tier between wood and iron, as in Raspberry Flavoured. That makes
copper worth mining from the first hour and gives stage 1 its own material. Done by datapack:
remove the stone tool recipes, and check what else uses stone tools (loot tables, villager
trades, mod recipes) so nothing points at an item players can no longer make.

**Enchanting without experience.** Modest Magic replaces the enchanting table with an altar
and pedestals. Items on the pedestals infuse an Enchanting Tablet, and the tablet is applied
at a smithing table, giving each enchantment it covers at exactly level one. Its description
names no experience cost, and its altar recipes are data driven, so the price is ingredients
we choose. To make that the only way:

- remove the vanilla enchanting table recipe, so luck and levels are out
- decide the anvil: no book combining (tablets replace books) and whether repair costs levels
- decide enchanted books from loot and villager trades
- verify in game first that Modest Magic itself charges no levels, since the description is
  the only evidence so far

**Tools last longer and work faster.** Raspberry Flavoured's balance here, which was good:
higher tool durability and quicker harvesting, so the longer early game does not turn into a
chore. Numbers are to be set by playing, starting near RF's. Likely routes, to verify:

- durability: an item's maximum damage is a default component that a 1.21.1 datapack cannot
  change, so this goes in the small Kotlin mod, through Fabric API's
  DefaultItemComponentEvents, one table of item to durability
- harvesting: the player.block_break_speed attribute (added in 1.21), raised for everyone by a
  datapack function or by the same mod

## The guide: our own advancement tree

Decided: no quest mod. The guide is a custom advancement tree written for this pack, in the
style of Raspberry Flavoured (https://raspberryflavoured.wiki.gg/wiki/Raspberry_Flavoured),
whose "completely custom set of advancements" guides players through progression and
mechanics.

- a "wly" tab, the heart as its icon, shipped as a datapack
- one branch per stage, each advancement asking for something real (craft a cutting board,
  power an Oritech machine) and saying why the next thing matters
- plain JSON reviewable in git, the same files on 1.21.1 and 26.x, rewards as functions
- wly already posts advancements to the Discord feed with a map of where they happened, so
  every milestone is a feed post
- in-game info for items through EMI, which the pack already ships, the way RF uses it

A quest mod was considered and set aside (FTB Quests works through packwiz from CurseForge,
tested 2026-10-19, then dropped). A **teams** mod may come later, once multiplayer needs
shared progress. Not now.

## End-less (PLANNED, leaning yes)

Raspberry Flavoured removes the End and almost everything tied to it (strongholds, end
portals, chorus fruit, shulkers, elytra) and replaces what it gave with gentler things:
paragliders as "safer, slower Elytras". It also swaps luck for determinism: no enchanting
table, tablets instead. That fits this pack already, since Modest Magic enchants with
tablets at an altar.

If adopted, the late game ends in stage 5 (infrastructure) instead of a dragon, and these need
deciding first:

- what replaces elytra travel and shulker storage, which players will miss
- the live world: has anyone been to the End, and what happens to elytra or shulker boxes
  already owned
- how it is removed: a datapack that removes the structures and recipes, or a mod

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
2. **Stages 1 to 3 legible:** the advancement tree for stages 1 to 3, steel gated on
   Oritech, item transport. Decide End-less.
3. **Stage 4:** Modest Magic and the cooking mods tied in with cross-ingredients.
4. **Launch readiness:** a domain, port 25565 opened on purpose (the whitelist is really on
   now), the off-box backup target set, view distance checked against real load. These live
   in weloveyou.mc's CLAUDE.md.
5. **Launch.** Stage 5 is designed once there are players to build it for.

## Avoid

- a linear advancement chain that locks content: the tree guides, it does not gate
- gating vanilla basics: people leave a pack that hides iron
- building stage 5 economy features before anyone is there to use them
