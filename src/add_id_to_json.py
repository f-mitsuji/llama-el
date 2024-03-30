import json
from pathlib import Path

file_path_obj = Path("result/simpleqs/llama-2-70b/wikipedia_url.json")

with file_path_obj.open(encoding="utf-8") as f:
    data = json.load(f)

for i, item in enumerate(data):
    item["id"] = i + 1

with file_path_obj.open(mode="w", encoding="utf-8") as f:
    json.dump(data, f)
