import replicate
from dotenv import load_dotenv
from pipeline.data_reader import get_prompt, read_json_file

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


def write_json_file(output_file_path, data, model, dataset):
    with open(output_file_path, "a", encoding="UTF-8") as output_file:
        output_file.write("[")
        data_length = len(data)
        for i, item in enumerate(data, start=1):
            input_text = item.get("utterance", None)

            if input_text is not None and input_text != "n/a":
                output = ChatCompletion(
                    model,
                    prompt=get_prompt(dataset, input_text),
                    system_prompt="Extract named entities from the following text and provide their Wikipedia URLs"
                )
            else:
                output = '"entities_text": [], "wikipedia_urls": []'

            output_file.write(f'{{"index": {i}, {output}}}')

            if i < data_length:
                output_file.write(",")
            output_file.write("\n")
        output_file.write("]")


def entity_wikipedia_url_extractor(model, dataset):
    # INPUT_FILE_PATH = 'datasets/test_datasets/' + dataset + '_test.json'
    INPUT_FILE_PATH = 'datasets/test_datasets/test.json'
    OUTPUT_FILE_PATH = 'result/' + dataset + '/' + model + '/wikipedia_url.json'
    data = read_json_file(INPUT_FILE_PATH)
    model = "meta/" + model + "-chat"
    write_json_file(OUTPUT_FILE_PATH, data, model, dataset)
