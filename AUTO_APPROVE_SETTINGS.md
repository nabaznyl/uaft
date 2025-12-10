# Auto-Approve Settings Configuration Guide

**Last Updated:** November 24, 2025  
**Status:** ✅ Code-Based Configuration  
**Format:** JSON (settings.json only - no text-based documents)

---

## Overview

Auto-approve settings in VS Code Copilot are managed exclusively through **settings.json** (code-based configuration), not through markdown documents. This ensures:
- ✅ Machine-readable configuration
- ✅ No human error or interpretation issues
- ✅ Automatic VS Code enforcement
- ✅ Version control friendly

---

## Configuration Location

**File:** `/root/.config/Code/User/settings.json` (or equivalent on your system)

**In VS Code UI:**
1. Open Settings (Ctrl+,)
2. Search for: `chat.autoApprove`
3. Enable the checkbox or edit JSON directly

---

## Current Settings

### Global Auto-Approve

```json
"chat.autoApprove": true
```

**Effect:** Automatically approve non-destructive chat operations globally.

### Terminal Command Auto-Approval

```json
"chat.tools.terminal.autoApprove": {
    "/.*": true
}
```

**Effect:** Automatically approve terminal commands matching the pattern `.*` (all commands).

**Alternative (safer):** Whitelist specific commands:
```json
"chat.tools.terminal.autoApprove": {
    "/^(ls|cat|echo|pwd|grep)\\s/": true,
    "/^(mv|cp|rm)\\s+/": false
}
```

### Approved Commands Whitelist

```json
"chat.tools.terminal.approvedCommands": {
    "ls": true,
    "cat": true,
    "echo": true,
    "pwd": true,
    "grep": true,
    "git": true,
    "python": true,
    "npm": true,
    "bash": true,
    "rm": true,
    "cp": true,
    "mv": true,
    "mkdir": true,
    "chmod": true,
    ...
}
```

**Effect:** Commands in this list with `true` value are auto-approved.

---

## Why Code-Based Only?

### ❌ Text-Based Markdown Documents (DON'T USE)

Previously, we attempted to use markdown files like `AUTO_APPROVE_SETTINGS.md` to document settings. This approach has critical issues:

1. **Not machine-readable** - Requires manual interpretation
2. **No enforcement** - VS Code can't enforce markdown rules
3. **Easy to forget** - Documents can get out of sync
4. **Misleading** - Appears to configure when it doesn't
5. **Maintenance burden** - Requires manual synchronization

### ✅ Code-Based JSON Configuration (USE THIS)

Settings.json is the correct approach because:

1. **Machine-readable** - VS Code parses and enforces automatically
2. **Enforced by default** - Settings take effect immediately
3. **Version controlled** - Changes tracked in git
4. **Auditable** - Clear configuration state at any point
5. **Programmatic** - Can be updated via scripts

---

## Setup Instructions

### Option 1: UI-Based (Easiest)

1. Open VS Code Settings (Ctrl+,)
2. Search: `chat.autoApprove`
3. Check the box to enable
4. VS Code automatically saves to settings.json

### Option 2: Direct JSON Editing

1. Open Command Palette (Ctrl+Shift+P)
2. Type: "Open User Settings (JSON)"
3. Add/update entries (see below)
4. Save file

### Option 3: Programmatic (Scripts)

```bash
# Example: Enable auto-approve via command line
SETTINGS_FILE="$HOME/.config/Code/User/settings.json"

# Using jq (if installed)
jq '.["chat.autoApprove"] = true' "$SETTINGS_FILE" > "$SETTINGS_FILE.tmp"
mv "$SETTINGS_FILE.tmp" "$SETTINGS_FILE"
```

---

## Complete Configuration Template

```json
{
    "chat.autoApprove": true,
    "chat.tools.terminal.autoApprove": {
        "/.*": true
    },
    "chat.tools.terminal.approvedCommands": {
        "ls": true,
        "cat": true,
        "echo": true,
        "pwd": true,
        "head": true,
        "tail": true,
        "grep": true,
        "find": true,
        "git": true,
        "git status": true,
        "git log": true,
        "git diff": true,
        "git branch": true,
        "git checkout": true,
        "git add": true,
        "git commit": true,
        "git push": true,
        "python": true,
        "python3": true,
        "pip": true,
        "npm": true,
        "node": true,
        "bash": true,
        "sh": true,
        "rm": true,
        "cp": true,
        "mv": true,
        "mkdir": true,
        "chmod": true,
        "chown": false,
        "sudo": false,
        "su": false
    },
    "chat.agent.maxRequests": 125
}
```

---

## Safety Levels

### 🟢 Maximum Permissiveness (All Auto-Approved)

```json
"chat.autoApprove": true,
"chat.tools.terminal.autoApprove": {
    "/.*": true
}
```

**Use when:** Development environment, trusted context  
**Risk:** Any command is auto-approved (including destructive ones)

### 🟡 Balanced (Commands Whitelisted)

```json
"chat.autoApprove": true,
"chat.tools.terminal.autoApprove": {
    "/^(ls|cat|echo|pwd|grep)\\s/": true
},
"chat.tools.terminal.approvedCommands": {
    "python": true,
    "npm": true,
    "git": true,
    "rm": false,
    "sudo": false
}
```

**Use when:** Production environment, careful selection  
**Risk:** Only explicitly whitelisted commands are approved

### 🔴 Maximum Safety (Manual Approval)

```json
"chat.autoApprove": false,
"chat.tools.terminal.autoApprove": {
    "/.*": false
}
```

**Use when:** High-security environment, financial systems  
**Risk:** All operations require manual approval (slower workflow)

---

## Troubleshooting

### Issue: Auto-approve not working

**Symptom:** Commands still require manual approval despite settings being enabled.

**Solutions:**

1. **Verify settings.json is valid JSON**
   ```bash
   # On Linux/Mac
   jq . ~/.config/Code/User/settings.json > /dev/null
   
   # On Windows
   python -m json.tool %APPDATA%/Code/User/settings.json
   ```

2. **Check for duplicate keys**
   - Remove any duplicate `"chat.autoApprove"` entries
   - Keep only one global definition

3. **Reload VS Code**
   - Close all VS Code windows
   - Reopen VS Code
   - Changes take effect on restart

4. **Check chat context**
   - Some chats may have per-conversation settings
   - Check chat preferences in UI

5. **Verify terminal tool is enabled**
   ```json
   "chat.tools.terminal.enable": true
   ```

### Issue: Too many commands approved

**Solution:** Use whitelist approach (🟡 Balanced above)

### Issue: Specific command not approved

**Solution:** Add to `approvedCommands` whitelist:
```json
"chat.tools.terminal.approvedCommands": {
    "mycommand": true
}
```

---

## Version Control Recommendations

### Do (✅)
- Commit `settings.json` to `.gitignore` for personal settings
- Keep workspace-level settings in `.vscode/settings.json` (repo-level)
- Document required settings in `CONTRIBUTING.md`

### Don't (❌)
- Store sensitive credentials in settings.json
- Commit personal auto-approve settings to repos
- Use text documents as configuration source

### Best Practice

In shared repos, document in CONTRIBUTING.md:
```markdown
### Recommended VS Code Settings

Add to your personal `settings.json`:

\`\`\`json
{
    "chat.autoApprove": true,
    "chat.tools.terminal.autoApprove": {"/.*": true},
    "chat.autoApprove.denylist": ["rm", "sudo", "reboot"]
}
\`\`\`
```

---

## Integration with UAFT

UAFT cleanup features can be auto-approved by adding:

```json
"chat.tools.terminal.approvedCommands": {
    "uaft cleanup": true,
    "/^uaft cleanup --profile=/": true,
    "/^uaft cleanup --execute$/": false
}
```

This allows auto-cleanup for non-destructive analysis, but requires manual approval for execution.

---

## FAQ

**Q: Is auto-approve safe?**  
A: Yes, if you understand what's being approved. Use whitelist approach for safety.

**Q: Can I have different settings per project?**  
A: Yes! Use `.vscode/settings.json` in workspace root for project-specific settings.

**Q: How do I disable auto-approve for specific commands?**  
A: Set them to `false` in `approvedCommands`:
```json
"chat.tools.terminal.approvedCommands": {
    "rm": false,
    "sudo": false
}
```

**Q: Do I need markdown documents for this?**  
A: No. JSON configuration in settings.json is the source of truth. Markdown is documentation only.

**Q: How is this different from the old approach?**  
A: The old approach used text-based markdown documents that weren't machine-readable. This approach uses code-based JSON that VS Code enforces automatically.

---

## Summary

✅ **Correct Approach (Use This):**
- Edit `~/.config/Code/User/settings.json`
- Set `"chat.autoApprove": true`
- Configure `chat.tools.terminal.approvedCommands` whitelist
- VS Code automatically enforces settings

❌ **Incorrect Approach (Don't Use):**
- Create text documents like `AUTO_APPROVE_SETTINGS.md`
- Expect them to configure anything (they don't)
- Manually check documents for settings
- Use markdown as configuration source

---

**Status:** ✅ Auto-Approve Configured  
**Last Test:** November 24, 2025  
**Next Review:** When adding new auto-approved commands

