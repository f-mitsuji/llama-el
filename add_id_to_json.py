import json

file_path = ""  # idをつけるファイル名 例）"result/simpleqs/llama-2-70b/wikipedia_url.json"

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

for i, item in enumerate(data):
    item["id"] = i + 1

with open(file_path, "w") as file:
    json.dump(data, file, indent=4)
