# Smart Caps Shortcut for Windows

Global hotkeys for fixing the case of selected text — anywhere you can type.

The headline trick: caps-lock typo `mY NAME is jOHN dOE` → select → **Ctrl+Alt+R** →
`My Name is John Doe`. Brands stay in their canonical form (`iphone` → `iPhone`),
acronyms stay all-caps (`gpu` → `GPU`), URLs and code identifiers are left alone.

AutoHotkey v2 utility, ~600 lines. System tray icon, configurable hotkeys.
Python sibling exists for reference.

## Hotkeys

| Hotkey | Transform | Example |
| --- | --- | --- |
| `Ctrl+Alt+R` | Smart Repair | `mY NAME is jOHN dOE` → `My Name is John Doe` |
| `Ctrl+Alt+T` | Title Case (smart — knows brands & acronyms) | `built with fastapi on the cdn` → `Built With FastAPI On The CDN` |
| `Ctrl+Alt+U` | UPPERCASE | `hello` → `HELLO` |
| `Ctrl+Alt+L` | lowercase | `HELLO` → `hello` |
| `Ctrl+Alt+K` | tOGGLE cASE | `Hello` → `hELLO` |
| `Ctrl+Alt+S` | snake_case | `getUserName` → `get_user_name` |
| `Ctrl+Alt+M` | camelCase | `user-profile` → `userProfile` |

All configurable in [src/config.ini](src/config.ini).

## Install

1. Install AutoHotkey v2:

   ```powershell
   winget install --id AutoHotkey.AutoHotkey -e
   ```

2. Clone or download this repo.
3. Double-click [start.cmd](start.cmd). Tray icon appears in ~1 second.

Auto-start on every login (one-time setup):

```powershell
$wshShell = New-Object -ComObject WScript.Shell
$lnk = $wshShell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\TextTransformer.lnk")
$lnk.TargetPath = "$PWD\start.cmd"; $lnk.WorkingDirectory = "$PWD"; $lnk.WindowStyle = 7; $lnk.Save()
```

## Smart Repair rules

For each whitespace-separated token in the selection:

| Token | Repair |
| --- | --- |
| URL (`https://…`, `mailto:…`) or email | leave alone |
| Has `_`, `/`, `\` (looks like code/path) | leave alone |
| Lowercased form is in the brand list | canonical form (`iPhone`) |
| Standalone `i` / `I` | `I` |
| All-caps and in the acronym list | leave alone |
| All-lowercase | leave alone (presumed intentional) |
| Anything else | `Firstuppercase rest lowercase` |

Brand list (~170) and acronym list (~740) live in `[Repair]` in
[src/config.ini](src/config.ini). Edit, then tray right-click → **Reload config**.

## Where it works (and doesn't)

**Works** in any app that honors Ctrl+C/V: VS Code, IntelliJ, Notepad, browsers
(address bar AND text fields), Gmail, Slack, Discord, Word, Outlook, Excel,
Teams, WhatsApp Web, Notion, Obsidian, Windows Terminal, PowerShell.

**Doesn't work**:

- Password fields — Windows blocks programmatic paste.
- Elevated apps when running un-elevated — UIPI blocks input injection.
- RDP — `rdpclip.exe` is flaky; bump `RestoreDelay` if needed.
- Some legacy console apps that ignore Ctrl+V.

## Layout

```
src/
  TextTransformer.ahk     - main implementation (AHK v2)
  config.ini              - hotkeys + brand/acronym lists
  text_transformer.py     - Python sibling (reference)
  requirements.txt
tests/test_transforms.py  - pytest for the pure transform functions
tests/manual_test_plan.md - hotkey/clipboard checklist
start.cmd                 - launcher (double-click to run)
```

## Tests

```powershell
pip install pytest
pytest tests/
```

Pure functions only — no keyboard or clipboard side-effects, runs anywhere.
The full hotkey path is in [tests/manual_test_plan.md](tests/manual_test_plan.md).

## License

MIT — see [LICENSE](LICENSE).
