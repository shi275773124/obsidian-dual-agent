# Obsidian Git Plugin Settings

Recommended config for the dual-agent vault.

## Install

1. Obsidian → Settings → **Community plugins** → **Turn on community plugins**
2. **Browse** → search **Obsidian Git** by Vinzent → **Install** → **Enable**

## Settings

Settings → **Obsidian Git**:

| Setting | Value | Reason |
|---|---|---|
| Vault backup interval (minutes) | `10` | Auto-push every 10 min |
| Auto pull interval (minutes) | `5` | Auto-pull every 5 min |
| Pull updates on startup | `on` | Sync immediately when Obsidian opens |
| Disable push | `off` | We want push enabled |
| Sync method | `merge` | Simpler than rebase for casual use |
| Commit message | `vault backup: {{date}}` | Distinguishable from agent commits |
| Commit author name | (your name) | Tells `git log` it's the human |
| Commit author email | (your email) | Tells `git log` it's the human |

## Why these intervals

- **Pull every 5 min, push every 10 min** = pull is more frequent than push, so you read the latest before writing.
- Faster intervals (1 min) generate commit spam.
- Slower (30+ min) means you can sit on stale agent edits when reviewing.

## Optional: hotkeys

Settings → Hotkeys → search "Obsidian Git":

- **Obsidian Git: Commit all changes** → `Cmd/Ctrl + Shift + S`
- **Obsidian Git: Pull** → `Cmd/Ctrl + Shift + P`
- **Obsidian Git: Push** → `Cmd/Ctrl + Shift + Up`

Lets you force a sync without waiting for the timer.

## Authentication

The plugin uses your system git's auth. So:

- **macOS / Linux**: SSH agent + key works out of the box
- **Windows**: easiest is HTTPS + PAT
  - Generate at https://github.com/settings/tokens (classic, scope `repo`)
  - `git remote set-url origin https://YOUR-PAT@github.com/you/agent-vault.git`
  - Or use Git Credential Manager (ships with Git for Windows)

## Troubleshooting

- Plugin not syncing? Click the **source-control sidebar icon** (left ribbon) to force pull/push.
- Conflicts? See [docs/04-troubleshooting.md](../docs/04-troubleshooting.md).
- Auth failing? Test git outside Obsidian first: `git pull` in a terminal at the vault path.
