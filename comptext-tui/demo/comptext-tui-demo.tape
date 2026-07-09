# VHS Tape - CompText TUI Demo Recording
# Render with: vhs comptext-tui/demo/comptext-tui-demo.tape

Output comptext-tui/assets/comptext-tui-demo.gif

Set FontSize 14
Set Width 900
Set Height 550
Set Padding 10
Set Theme "Dracula"
Set PlaybackSpeed 1.0

# Initial sleep
Sleep 1s

# Navigate and print help
Type "node comptext-tui/dist/cli.js /help"
Enter
Sleep 3s

# Check status
Type "node comptext-tui/dist/cli.js /status"
Enter
Sleep 3s

# Check doctor diagnostics
Type "node comptext-tui/dist/cli.js /doctor"
Enter
Sleep 3s

# Unrecognized command check (expected failure)
Type "node comptext-tui/dist/cli.js /unknown-command"
Enter
Sleep 4s
