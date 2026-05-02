# Manual test plan

The clipboard/hotkey path can't be unit-tested. Walk this once before each release.

## Smart Repair (the headline)

| Type, select all, **Ctrl+Alt+R** | Expect |
| --- | --- |
| `mY NAME is jOHN dOE` | `My Name is John Doe` |
| `URGENT MEETING NOTES` | `Urgent Meeting Notes` |
| `the GPU runs hot` | unchanged (acronym preserved) |
| `WRITTEN IN JAVASCRIPT` | `Written In JavaScript` |
| `i think i can` | `I think I can` |
| `see https://Example.COM/path` | unchanged (URL skipped) |
| `call get_user_name()` | unchanged (identifier skipped) |

## Mechanical transforms

Type `hello world`, select, hit each:

- `Ctrl+Alt+U` → `HELLO WORLD`
- `Ctrl+Alt+L` → `hello world`
- `Ctrl+Alt+T` → `Hello World`
- `Ctrl+Alt+K` → `hELLO wORLD`

Then with `helloWorld` selected: `Ctrl+Alt+S` → `hello_world`. Then with `hello_world` selected: `Ctrl+Alt+M` → `helloWorld`.

## Clipboard preservation

Copy `important` to clipboard. In Notepad: type `mY MESSED uP TEXT`, select, `Ctrl+Alt+R`. Switch window, `Ctrl+V` — should paste `important`.

## No selection / non-text

Empty editor, no selection, `Ctrl+Alt+R` → tooltip "No text selected". Take a screenshot via Win+Shift+S, then `Ctrl+Alt+R` in an empty editor → same tooltip; image still in clipboard.

## Cross-app

Repeat the headline test in: VS Code, Chrome address bar, a Chrome textarea (Gmail compose), Slack, Discord, Word, Outlook compose, Windows Terminal. If any fail, raise `RestoreDelay` in `config.ini` and reload.

## Known-bad targets

These should fail gracefully (no clipboard corruption):

- Password fields (Windows blocks programmatic paste)
- Elevated windows when running un-elevated (UIPI block)
- RDP sessions (rdpclip flakes)

## Large input

500 KB block in Notepad, Ctrl+A, `Ctrl+Alt+L` → no UI freeze >1s. Set `MaxLength=10000`, reload, repeat → tooltip "Selection too large".

## Tray menu

Right-click tray → Enabled (uncheck) → hotkey does nothing. Re-check. Edit config → change `Repair=^!r` to `^!q` → Reload → Ctrl+Alt+Q now repairs, Ctrl+Alt+R doesn't.

## Custom brand

Append `,Acme` to `Brands=` in config.ini. Reload. Type `acme` in Notepad, select, `Ctrl+Alt+R` → `Acme`.

## Rapid repeat

Hold `Ctrl+Alt+R` on a selection for ~1 s. At most one transform in flight at a time (busy guard); no clipboard corruption.
