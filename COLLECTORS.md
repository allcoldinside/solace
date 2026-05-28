# Collector System (24 bots)

SOLACE uses a canonical 24-bot collector system.

## IDs
`SPIDER-1` through `SPIDER-24`

Defined in:
- `collectors/__init__.py` (`COLLECTOR_BOT_IDS`)
- `collectors/seed_collector.py` for deterministic seed output

## Behavior
Each collector emits normalized items with:
- `source` (`seed:<bot_id>`)
- `content`
- `target`
- `target_type`
- `collector_id`

## Extending with real collectors
To replace seed behavior:
1. Keep the same `bot_id` registry and interface.
2. Implement per-bot source adapters behind `BaseCollector.collect()`.
3. Preserve output schema compatibility so pipeline stages remain unchanged.
