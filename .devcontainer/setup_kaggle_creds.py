# This script ensures Kaggle CLI credentials are available in ~/.kaggle/kaggle.json
import os, json, pathlib

kaggle_dir = pathlib.Path.home() / ".kaggle"
kaggle_dir.mkdir(exist_ok=True)

kaggle_json = kaggle_dir / "kaggle.json"
creds = {
    "username": os.environ.get("KAGGLE_USERNAME", ""),
    "key": os.environ.get("KAGGLE_KEY", ""),
}
with open(kaggle_json, "w") as f:
    json.dump(creds, f)
os.chmod(kaggle_json, 0o600)
print(f"Kaggle credentials written to {kaggle_json}")
