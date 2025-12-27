import hashlib, json, os

REPO_USER = "ThatGuyJack01"
REPO_NAME = "GodSMP-Pack"
BRANCH = "main"
MODS_DIR = "mods"

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

mods = []

for fname in os.listdir(MODS_DIR):
    if not fname.endswith(".jar"):
        continue

    mods.append({
        "id": fname.split("-")[0],
        "fileName": fname,
        "url": f"https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/{BRANCH}/{MODS_DIR}/{fname}",
        "sha256": sha256(os.path.join(MODS_DIR, fname)),
        "required": True
    })

manifest = {
    "packId": "godsmp-pack",
    "packVersion": "auto",
    "mods": mods
}

with open("manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

print("manifest.json regenerated")