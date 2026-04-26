# Panel System (8 analysts)

SOLACE runs an 8-analyst panel stage after report generation.

## IDs
- ANALYST-ALPHA
- ANALYST-BRAVO
- ANALYST-CHARLIE
- ANALYST-DELTA
- ANALYST-ECHO
- ANALYST-FOXTROT
- ANALYST-GOLF
- ANALYST-HOTEL

Defined in `panel/models.py` as `PANEL_BOT_IDS`.

## Current scaffold behavior
`panel/engine.py` builds a deterministic transcript entry from each bot for the report subject.

## Upgrade path
You can map each analyst ID to a dedicated prompt/model pair while keeping:
- transcript list output
- panel summary output
- `bots_used` metadata
