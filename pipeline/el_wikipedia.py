import replicate
from dotenv import load_dotenv
from pipeline.data_reader import get_few_shots, read_dataset_file

load_dotenv()


def ChatCompletion(model, prompt, system_prompt):
    output = replicate.run(
        model,
        input={
            "system_prompt": system_prompt,
            "prompt": prompt,
            "temperature": 0.01}
    )
    return "".join(output)


def write_json_file(output_file_path, data, model, system_prompt, dataset):
    with open(output_file_path, "a", encoding="UTF-8") as output_file:
        output_file.write("[")
        data_length = len(data)
        for i, item in enumerate(data, start=1):
            if dataset == "lcquad2":
                input_text = item.get("question", None)
            elif dataset == "simpleqs":
                input_text = item.split("\t")[3]
            elif dataset == "webqsp":
                input_text = item.get("utterance", None)

            if input_text is not None and input_text != "n/a":  # データセットのEL対象文に空値と'n/a'がある
                output = ChatCompletion(                        # その場合要素が空値のデータを返す
                    model,
                    prompt=f'''INPUT: {input}\nOUTPUT:''',
                    system_prompt=system_prompt
                )
            else:
                output = '"entities_text": [], "wikipedia_urls": []'

            output_file.write(f'{{"index": {i}, {output}}}')

            if i < data_length:
                output_file.write(",")
            output_file.write("\n")
        output_file.write("]")


def entity_wikipedia_url_extractor(model, dataset):
    # INPUT_FILE_PATH = f'datasets/test_datasets/{dataset}_test.json'
    INPUT_FILE_PATH = 'datasets/test_datasets/test.json'
    OUTPUT_FILE_PATH = f'result/{dataset}/{model}/wikipedia_url.json'
    data = read_dataset_file(dataset, INPUT_FILE_PATH)
    model = f"meta/{model}-chat"
    system_prompt = f'''Extract named entities from the text and provide their Wikipedia URLs according to the following examples.
Never output any sentences, explanations or reasons other than the value of each key.

examples:
{get_few_shots(dataset)}'''
    write_json_file(OUTPUT_FILE_PATH, data, model, system_prompt, dataset)
