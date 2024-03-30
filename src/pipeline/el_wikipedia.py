import re
import time
from pathlib import Path

import replicate
import torch
from dotenv import load_dotenv
from pipeline.data_reader import get_few_shots, read_dataset_file
from transformers import AutoModelForCausalLM, AutoTokenizer

load_dotenv()


def chat_completion_replicate(model: str, prompt: str, system_prompt: str) -> str:
    output = replicate.run(model, input={"system_prompt": system_prompt, "prompt": prompt, "temperature": 0.01})
    return "".join(output)


def chat_completion_swallow(
    instruction: str, input_text: str, model: AutoModelForCausalLM, tokenizer: AutoTokenizer
) -> str:
    prompt_template = (
        "以下に、あるタスクを説明する指示があり、それに付随する入力が更なる文脈を提供しています。"
        "リクエストを適切に完了するための回答を記述してください。\n\n"
        "### 指示:\n{instruction}\n\n入力: {input}\n出力:"
    )
    prompt = prompt_template.format(instruction=instruction, input=input_text)

    input_ids = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
    tokens = model.generate(
        input_ids.to(model.device),
        max_new_tokens=128,
        temperature=0.01,
        # top_p=0.95,
        do_sample=True,
    )

    generated_text = tokenizer.decode(tokens[0], skip_special_tokens=True)

    return generated_text[len(prompt) :].strip()


def extract_input_text(item: dict, dataset: str, language: str) -> str:
    if language == "japanese":
        return item.get("question")
    if dataset == "lcquad2":
        return item.get("question")
    if dataset == "simpleqs":
        return item.split("\t")[3]
    if dataset == "webqsp":
        return item.get("utterance")

    error_msg = f"Invalid dataset or language: {dataset}, {language}"
    raise ValueError(error_msg)


def get_output(input_text: str, language: str, model_name: str, system_prompt: str) -> str:
    if input_text is None or input_text == "n/a":
        return '{"entities_text": [], "wikipedia_urls": []}'

    if language == "english":
        output = chat_completion_replicate(
            model_name,
            prompt=f"""INPUT: {input_text}\nOUTPUT:""",
            system_prompt=system_prompt,
        )
        time.sleep(1)  # 最低0.1 2024/2/23
        return output

    if language == "japanese":
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=True,
            device_map="auto",
        )
        return chat_completion_swallow(system_prompt, input_text, model, tokenizer)

    msg = f"Unsupported language: {language}"
    raise ValueError(msg)


def write_json_file(
    output_file_path: Path,
    data: list[dict[str, str]] | list[str],
    model_name: str,
    system_prompt: str,
    dataset: str,
    language: str,
) -> None:
    with output_file_path.open(mode="a", encoding="UTF-8") as output_file:
        output_file.write("[")
        data_length = len(data)

        not_matching_count = 0

        for i, item in enumerate(data, start=1):
            input_text = extract_input_text(item, dataset, language)
            output = get_output(input_text, language, model_name, system_prompt)

            if not re.search(r'^"entities_text": \[.*\],\s*"wikipedia_urls": \[.*\]$', output, re.S):
                not_matching_count += 1
                print(f"Index not matching: {i}")

            if language == "japanese":
                output_file.write(f'{{"id": {i}, {output}}}')
            else:
                output_file.write(output)

            if i < data_length:
                output_file.write(",")
            output_file.write("\n")
        output_file.write("]")

        print(f"Total not matching: {not_matching_count}")


def get_config(language: str, dataset: str, model: str) -> dict:
    configs = {
        "english": {
            "file_extension": ".txt" if dataset == "simpleqs" else ".json",
            "model_prefix": "meta",
            "model_suffix": "-chat",
            "language_suffix": "",
            "system_prompt": (
                "Extract named entities from the text and provide their Wikipedia URLs, as in the examples below.\n"
                "Do not output any text other than the keys and values in JSON.\n\n"
                "examples:\n"
            ),
        },
        "japanese": {
            "file_extension": ".json",
            "model_prefix": "tokyotech-llm",
            "model_suffix": "-instruct-hf",
            "language_suffix": "_japanese",
            "system_prompt": """以下の例のように、テキストから固有表現を抽出し、それらのWikipediaのURLを示せ。
JSONのキーと値以外のテキストは出力しないでください。与えられた入力にのみ答えてください。
例:
""",
        },
    }

    if language not in configs:
        error_msg = "Unsupported language."
        raise ValueError(error_msg)

    config = configs[language]
    config["model"] = f"{config['model_prefix']}/{model}{config['model_suffix']}"
    config["system_prompt"] += get_few_shots(dataset, language)
    return config


def entity_wikipedia_url_extractor(model: str, dataset: str, language: str) -> None:
    config = get_config(language, dataset, model)
    # input_file_path = "datasets/test_datasets/test.json"
    # output_file_path = f"result/{dataset}/{model}/test.json"
    input_file_path = f"datasets/test_datasets/{dataset}{config['language_suffix']}_test{config['file_extension']}"
    output_file_path = Path(f"result/{dataset}/{model}/wikipedia_url.json")
    data = read_dataset_file(input_file_path)
    write_json_file(output_file_path, data, config["model"], config["system_prompt"], dataset, language)
