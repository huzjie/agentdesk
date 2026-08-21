"""HTTP healthcheck against the control plane."""
import sys
import urllib.request

try:
    with urllib.request.urlopen("http://127.0.0.1:8500/healthz", timeout=5) as r:
        print(r.read().decode())
        sys.exit(0 if r.status == 200 else 1)
except Exception as e:
    print(f"healthcheck failed: {e}")
    sys.exit(1)
