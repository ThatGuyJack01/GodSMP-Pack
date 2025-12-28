#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
from pathlib import Path
from typing import List


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def should_include(name: str, includes: List[str], excludes: List[str]) -> bool:
    if includes and not any(fnmatch.fnmatch(name, pat) for pat in includes):
        return False
    if excludes and any(fnmatch.fnmatch(name, pat) for pat in excludes):
        return False
    return True


def infer_id_from_filename(filename: str) -> str:
    base = filename[:-4] if filename.endswith(".jar") else filename
    return base.split("-", 1)[0] if "-" in base else base


def main() -> None:
    script_path = Path(__file__).resolve()
    tools_dir = script_path.parent
    repo_root = tools_dir.parent  # tools/.. = repo root

    ap = argparse.ArgumentParser(description="Generate manifest.json from local mods folder.")
    ap.add_argument(
        "--mods-dir",
        default=str(repo_root / "mods"),
        help="Directory containing .jar files (default: <repo_root>/mods)",
    )
    ap.add_argument(
        "--out",
        default=str(repo_root / "manifest.json"),
        help="Output manifest path (default: <repo_root>/manifest.json)",
    )
    ap.add_argument("--pack-id", default="godsmp-pack")
    ap.add_argument("--pack-version", default="dev")
    ap.add_argument(
        "--base-url",
        required=True,
        help="Base URL where jars are hosted (example: https://raw.githubusercontent.com/USER/REPO/main/mods)",
    )
    ap.add_argument("--include", action="append", default=[], help="Glob include")
    ap.add_argument("--exclude", action="append", default=[], help="Glob exclude")
    args = ap.parse_args()

    mods_dir = Path(args.mods_dir).resolve()
    out_path = Path(args.out).resolve()

    # Helpful debug output (so you always know what it's doing)
    print("Script:", script_path)
    print("Repo root (inferred):", repo_root)
    print("Mods dir:", mods_dir)
    print("Manifest out:", out_path)

    if not mods_dir.exists() or not mods_dir.is_dir():
        raise SystemExit(f"mods_dir does not exist or is not a directory: {mods_dir}")

    jars = [p for p in mods_dir.iterdir() if p.is_file() and p.name.endswith(".jar")]
    jars = [p for p in jars if should_include(p.name, args.include, args.exclude)]
    jars.sort(key=lambda p: p.name.lower())

    base_url = args.base_url.rstrip("/")

    mods = []
    for jar in jars:
        mods.append(
            {
                "id": infer_id_from_filename(jar.name),
                "fileName": jar.name,
                "url": f"{base_url}/{jar.name}",
                "sha256": sha256_file(jar),
                "required": True,
            }
        )

    manifest = {
        "packId": args.pack_id,
        "packVersion": args.pack_version,
        "mods": mods,
    }

    out_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote {out_path} with {len(mods)} mod(s).")


if __name__ == "__main__":
    main()
