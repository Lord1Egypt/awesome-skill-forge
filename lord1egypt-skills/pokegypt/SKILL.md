---
name: pokegypt
description: "Run and manage a PokeGypt TFS 1.2 Pokemon OT private server — SQLite backend, account manager, Linux/Windows."
version: 1.0.0
author: Lord1Egypt
license: MIT
platforms: [linux, windows]
category: gaming
tags: [pokemon, tfs, private-server, sqlite, game-server, otserver, pokegypt]
compatible: [claude-code, openai-agents, hermes-agent, autogen, langchain, any-llm]
source: lord1egypt
source_url: https://github.com/Lord1Egypt/PokeGypt
---

# pokegypt

Set up and operate a **PokeGypt** Pokemon OT private server based on TFS 1.2 with a SQLite backend (no MySQL required), a built-in account manager, and cross-platform support for Linux and Windows.

## Install

```bash
# Clone the server
git clone https://github.com/Lord1Egypt/PokeGypt
cd PokeGypt

# Linux — compile
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)

# Windows — use the pre-built binary in /bin
```

## Configuration

Edit `config.lua` to set server name, port, and world type:

```lua
serverName = "PokeGypt"
ip = "127.0.0.1"
port = 7171
worldType = "pvp"
sqliteDatabase = "db/pokegypt.db"
```

## Account Manager

The built-in account manager runs at port 7171. Connect with any Tibia/OT client:
- **Account:** 1 / **Password:** 1 to access the GM account
- Create player accounts via the in-game account manager NPC

## Start the Server

```bash
# Linux
./pokegypt

# Windows
pokegypt.exe
```

## Common Tasks

**Add a GM account:**
```sql
UPDATE accounts SET type = 5 WHERE id = 1;
```

**Reset a player's position (if stuck):**
```sql
UPDATE players SET posx=1000, posy=1000, posz=7 WHERE name='PlayerName';
```

**Backup the database:**
```bash
cp db/pokegypt.db db/pokegypt_backup_$(date +%Y%m%d).db
```

## Ports

| Port | Purpose |
|------|---------|
| 7171 | Login server + account manager |
| 7172 | Game world |

## Differences from Standard TFS

- **SQLite** instead of MySQL — zero database server setup
- **PokeGypt maps** — custom Pokemon-themed world
- **Cross-platform binary** — works on Linux and Windows without recompile
- Account manager NPC built-in — no external web panel needed
