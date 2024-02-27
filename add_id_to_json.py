import json

file_path = "result/lcquad2/llama-2-70b/wikipedia_url.json"
# file_path = 'datasets/test_datasets/lcquad2_test2.json'

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

for i, item in enumerate(data):
    item["id"] = i + 1

with open(file_path, "w") as file:
    json.dump(data, file, indent=4)
