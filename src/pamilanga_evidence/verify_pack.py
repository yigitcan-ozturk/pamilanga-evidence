"""Standalone integrity check for a supplied Evidence Pack directory."""
import argparse
import json
from pathlib import Path

from pamilanga_evidence.trace.run_verifier import verify_run


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a PAMILANGA Evidence Pack")
    parser.add_argument("pack_dir", type=Path)
    args = parser.parse_args()
    pack = args.pack_dir
    try:
        manifest = json.loads((pack / "manifest.json").read_text(encoding="utf-8"))
        stream_name = manifest.get("stream")
        if not isinstance(stream_name, str) or not stream_name or Path(stream_name).name != stream_name:
            raise ValueError("Invalid stream filename")
        result = verify_run(pack / stream_name, pack / "manifest.json")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result = {"status": "FAIL", "reason": "PACK_READ_ERROR", "detail": str(exc)}
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
