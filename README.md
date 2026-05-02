# Smart Caps Shortcut for Windows

A small utility with global hotkeys for fixing the case of selected text. Works in any app that handles Ctrl+C and Ctrl+V.

The main one is Ctrl+Alt+R. If caps lock was half-on and you typed `mY NAME is jOHN dOE`, select it and press Ctrl+Alt+R. You get back `My Name is John Doe`. Brand names like `iphone` get fixed to `iPhone`, acronyms like `gpu` stay as `GPU`, and URLs or things that look like code are left alone.

It's an AutoHotkey v2 script. There's also a Python port in the repo for reference.

## Hotkeys

| Key | Does | Example |
|---|---|---|
| Ctrl+Alt+R | Smart Repair | `mY NAME is jOHN dOE` → `My Name is John Doe` |
| Ctrl+Alt+T | Title Case | `built with fastapi on the cdn` → `Built With FastAPI On The CDN` |
| Ctrl+Alt+U | UPPERCASE | `hello` → `HELLO` |
| Ctrl+Alt+L | lowercase | `HELLO` → `hello` |
| Ctrl+Alt+K | Toggle | `Hello` → `hELLO` |
| Ctrl+Alt+S | snake_case | `getUserName` → `get_user_name` |
| Ctrl+Alt+M | camelCase | `user-profile` → `userProfile` |

Change them in [src/config.ini](src/config.ini) if you want.

## Install

Install AutoHotkey:

```
winget install --id AutoHotkey.AutoHotkey -e
```

Clone the repo, then double-click [start.cmd](start.cmd). The tray icon will appear.

To make it run every time you log in:

```powershell
$wshShell = New-Object -ComObject WScript.Shell
$lnk = $wshShell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\TextTransformer.lnk")
$lnk.TargetPath = "$PWD\start.cmd"
$lnk.WorkingDirectory = "$PWD"
$lnk.WindowStyle = 7
$lnk.Save()
```

## How Smart Repair decides

For each word in the selection:

- URL or email: untouched
- Has `_`, `/`, `\` in it: untouched, looks like code
- Matches a brand: replaced with the canonical form (`iphone` becomes `iPhone`)
- Just `i` or `I` on its own: capitalized
- All caps and a known acronym: kept as is
- All lowercase: kept as is, probably intentional
- Anything else: first letter capitalized, rest lowercased

About 170 brand names and 740 acronyms ship with it. They live in [src/config.ini](src/config.ini) under `[Repair]`. Add your own, then right-click the tray icon and pick Reload config.

## Where it works

Most apps that take Ctrl+C and Ctrl+V. VS Code, Notepad, browsers (address bar and text fields), Gmail, Slack, Discord, Word, Outlook, Teams, Notion, terminals.

Where it won't:

- Password fields. Windows blocks paste programmatically.
- Elevated apps when you're not running elevated. Same security barrier.
- RDP. Clipboard sync over RDP is unreliable. Bump RestoreDelay in config.ini.
- Some old console apps that ignore Ctrl+V.

## Files

```
src/
  TextTransformer.ahk     main script
  config.ini              hotkeys and lists
  text_transformer.py     Python port (reference)
  requirements.txt
tests/
  test_transforms.py      pytest
  manual_test_plan.md     hotkey/clipboard checklist
start.cmd                 launcher
```

## Tests

```
pip install pytest
pytest tests/
```

These only cover the pure functions. The hotkey and clipboard side needs to be tested by hand, see [tests/manual_test_plan.md](tests/manual_test_plan.md).

## License

MIT. See [LICENSE](LICENSE).
