#!/usr/bin/env python3
"""Hook: PreToolUse(Bash) — guard against dangerous commands.

Effect: before a Bash command runs, blocks obviously destructive commands (recursive delete of /,
        formatting a disk, fork bombs) with exit code 2 and explains why. Only a high-risk deny list
        is blocked; everything else passes (fail open).
Note:   a thin safety net, not a substitute for care; adjust the patterns in DANGEROUS as needed.
"""
import json
import re
import sys

DANGEROUS = [
    r"\brm\s+-rf?\s+/(?:\s|$)",       # rm -rf /
    r"\brm\s+-rf?\s+~",                # rm -rf ~
    r"\brm\s+-rf?\s+\*",               # rm -rf * (wipe the current directory)
    r":\(\)\s*\{\s*:\|:&\s*\}\s*;",   # fork bomb :(){ :|:& };:
    r"\bmkfs\.",                       # format a file system
    r"\bdd\b.*\bof=/dev/",            # dd onto a raw device
    r">\s*/dev/sd[a-z]",              # redirect onto a raw disk
]


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if data.get("tool_name") != "Bash":
        sys.exit(0)

    command = (data.get("tool_input") or {}).get("command", "")
    for pat in DANGEROUS:
        if re.search(pat, command):
            print(
                f"[safety guard] blocked: the command matches a high-risk pattern ({pat}):\n{command}\n"
                f"If it is really necessary, a human should run it manually in a terminal.",
                file=sys.stderr,
            )
            sys.exit(2)  # block execution
    sys.exit(0)


if __name__ == "__main__":
    main()
