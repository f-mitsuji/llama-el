import time

import replicate
import torch
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer

from pipeline.data_reader import get_few_shots, read_dataset_file

load_dotenv()


def ChatCompletion_replicate(model: str, prompt: str, system_prompt: str) -> str:
    output = replicate.run(model, input={"system_prompt": system_prompt, "prompt": prompt, "temperature": 0.01})
    return "".join(output)


def ChatCompletion_swallow(system_prompt, input_text, model, tokenizer):
    prompt_template = "{system_prompt}" "入力:{input}" "出力:"
    prompt = prompt_template.format(system_prompt=system_prompt, input=input_text)

    input_ids = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
    tokens = model.generate(
        input_ids.to(model.device),
        max_new_tokens=128,
        temperature=0.01,
        top_p=0.95,
        do_sample=True,
    )
    generated_text = tokenizer.decode(tokens[0], skip_special_tokens=True)

    # 生成されたテキストからプロンプト部分を削除
    generated_response = generated_text[len(prompt) :].strip()

    return generated_response


# def ChatCompletion_swallow(instruction, input_text, model, tokenizer):
#     prompt_template = (
#         "以下に、あるタスクを説明する指示があり、それに付随する入力が更なる文脈を提供しています。"
#         "リクエストを適切に完了するための回答を記述してください。\n\n"
#         "### 指示:\n{instruction}\n\n### 入力:\n{input}\n\n### 応答:"
#     )
#     prompt = prompt_template.format(instruction=instruction, input=input_text)

#     input_ids = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
#     tokens = model.generate(
#         input_ids.to(model.device),
#         max_new_tokens=128,
#         temperature=0.01,
#         top_p=0.95,
#         do_sample=True,
#     )

#     return tokenizer.decode(tokens[0], skip_special_tokens=True)


def extract_input_text(item, dataset, language):
    if language == "japanese":
        return item.get("question", None)
    if dataset == "lcquad2":
        return item.get("question", None)
    elif dataset == "simpleqs":
        return item.split("\t")[3]
    elif dataset == "webqsp":
        return item.get("utterance", None)
    return None


def get_output(input_text, language, model_name, system_prompt):
    if input_text is None or input_text == "n/a":
        return '{"entities_text": [], "wikipedia_urls": []}'

    if language == "english":
        output = ChatCompletion_replicate(
            model_name, prompt=f"""INPUT: {input_text}\nOUTPUT:""", system_prompt=system_prompt
        )
        time.sleep(1)  # 最低0.1 2024/2/23
        return output
    elif language == "japanese":
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype=torch.bfloat16, low_cpu_mem_usage=True, device_map="auto"
        )
        return ChatCompletion_swallow(system_prompt, input_text, model, tokenizer)


# dataの型ヒントは扱うデータのみ
def write_json_file(
    output_file_path: str,
    data: list[dict[str, str]] | list[str],
    model_name: str,
    system_prompt: str,
    dataset: str,
    language: str,
) -> None:

    with open(output_file_path, "a", encoding="UTF-8") as output_file:
        output_file.write("[")
        data_length = len(data)

        for i, item in enumerate(data, start=1):
            input_text = extract_input_text(item, dataset, language)
            output = get_output(input_text, language, model_name, system_prompt)
            output_file.write(output)

            if i < data_length:
                output_file.write(",")
            output_file.write("\n")
        output_file.write("]")


def get_config(language: str, dataset: str, model: str) -> dict:
    configs = {
        "english": {
            "file_extension": ".txt" if dataset == "simpleqs" else ".json",
            "model_prefix": "meta",
            "model_suffix": "-chat",
            "system_prompt": """Extract named entities from the text and provide their Wikipedia URLs, as in the examples below.
Do not output any text other than the keys and values in JSON.

examples:
""",
        },
        "japanese": {
            "file_extension": ".json",
            "model_prefix": "tokyotech-llm",
            "model_suffix": "-instruct-hf",
            "system_prompt": """以下の例のように、テキストから固有表現を抽出し、それらのWikipediaのURLを示せ。
JSONのキーと値以外のテキストは出力しないでください。

例:
""",
        },
    }

    if language not in configs:
        raise ValueError("Unsupported language.")

    config = configs[language]
    config["model"] = f"{config['model_prefix']}/{model}{config['model_suffix']}"
    config["system_prompt"] += get_few_shots(dataset, language)
    return config


def entity_wikipedia_url_extractor(model: str, dataset: str, language: str) -> None:
    config = get_config(language, dataset, model)
    input_file_path = "datasets/test_datasets/test.json"
    output_file_path = f"result/{dataset}/{model}/test.json"
    # input_file_path = f"datasets/test_datasets/{dataset}_test{config['file_extension']}"
    # output_file_path = f"result/{dataset}/{model}/wikipedia_url.json"

    data = read_dataset_file(dataset, input_file_path)
    write_json_file(output_file_path, data, config["model"], config["system_prompt"], dataset, language)
