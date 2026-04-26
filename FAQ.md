# FAQ

## Does SOLACE require external APIs to run?
No. The seed collector path allows full end-to-end pipeline execution without external API credentials.

## Why do I see tenant_id `default`?
Single-tenant local mode defaults tenant context to `default` for easy local development.

## Why are there both API and worker processes?
API serves requests; worker processes execute asynchronous jobs and scalable background workloads.

## What does “8 and 24 bot systems” mean?
- 24 collector bots (`SPIDER-1..SPIDER-24`) in the collection stage.
- 8 panel analyst bots (`ANALYST-ALPHA..ANALYST-HOTEL`) in the panel stage.

## How do I reset local DB quickly?
If using SQLite locally, stop services and delete `solace.db`, then rerun migrations/setup.
