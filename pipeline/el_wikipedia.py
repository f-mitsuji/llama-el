from dotenv import load_dotenv
import replicate
import json

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


def read_json_file(file_path):
    with open(file_path, "r", encoding="UTF-8") as input_file:
        data = json.load(input_file)
        return data


def write_json_file(output_file_path, data, model):
    with open(output_file_path, "a", encoding="UTF-8") as output_file:
        output_file.write("[")
        data_length = len(data)
        for i, item in enumerate(data, start=1):
            input_text = item.get("utterance", None)

            if input_text is not None and input_text != "n/a":
                prompt = f'''INPUT: what does the letters eu stand for?
                OUTPUT: \"entities_text\": [], \"wikipedia_urls\": []
                INPUT: what country is the grand bahama island in?
                OUTPUT: \"entities_text\": [\"grand bahama\"], \"wikipedia_urls\": [\"https://en.wikipedia.org/wiki/Grand_Bahama\"]
                INPUT: what character did john noble play in lord of the rings?
                OUTPUT: \"entities_text\": [\"john noble\", \"lord of the rings\"], \"wikipedia_urls\": [\"https://en.wikipedia.org/wiki/John_Noble\", \"https://en.wikipedia.org/wiki/The_Lord_of_the_Rings:_The_Two_Towers\"]
                INPUT: what city is the state capital of washington?
                OUTPUT: \"entities_text\": [\"washington\"], \"wikipedia_urls\": [\"https://en.wikipedia.org/wiki/Washington_(state)\"]
                INPUT: {input_text}
                OUTPUT:'''
                output = ChatCompletion(
                    model,
                    prompt,
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
    write_json_file(OUTPUT_FILE_PATH, data, model)
