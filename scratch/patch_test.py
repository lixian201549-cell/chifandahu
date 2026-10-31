with open("scratch/test_meeting_conflicts.py", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace(
    "const console = { log: print, error: print, warn: print };",
    "const console = { log: print, error: print, warn: print };\nconst setTimeout = (fn) => 0;\nconst clearTimeout = () => {};\nconst setInterval = (fn) => 0;\nconst clearInterval = () => {};"
)

with open("scratch/test_meeting_conflicts.py", "w", encoding="utf-8") as f:
    f.write(c)

print("Patched scratch/test_meeting_conflicts.py")
