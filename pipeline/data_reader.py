import json


def read_dataset_file(dataset, file_path):
    if dataset in ["lcquad2", "webqsp"]:
        return read_json_file(file_path)

    elif dataset == "simpleqs":
        with open(file_path, "r", encoding="UTF-8") as input_file:
            data = list(input_file)
        return data


def read_json_file(file_path):
    with open(file_path, "r", encoding="UTF-8") as input_file:
        return json.load(input_file)


def read_correct_wikidata_ids(file_path, dataset):
    correct_wikidata_ids = []

    if dataset in ["lcquad2", "webqsp"]:
        data = read_json_file(file_path)

        for entry in data:
            entities = entry.get("entities", [])
            wikidata_ids = [entity for entity in entities if entity is not None]

            if not wikidata_ids:
                correct_wikidata_ids.append([""])
            else:
                correct_wikidata_ids.append(wikidata_ids)

        return correct_wikidata_ids

    elif dataset == "simpleqs":
        with open(file_path, "r", encoding="UTF-8") as file:
            for line in file:
                correct_wikidata_id = line.strip().split("\t")[0]
                correct_wikidata_ids.append(correct_wikidata_id)

        return correct_wikidata_ids


def read_predicted_wikidata_ids(file_path):
    predicted_wikidata_ids = []

    data = read_json_file(file_path)

    for entry in data:
        entities = entry.get("wikidata_ids", [])
        wikidata_ids = [entity for entity in entities if entity is not None]

        if not wikidata_ids:
            predicted_wikidata_ids.append([""])
        else:
            predicted_wikidata_ids.append(wikidata_ids)

    return predicted_wikidata_ids


def get_few_shots(dataset, language):
    responses = {
        (
            "english",
            "lcquad2",
        ): """INPUT: What does emigration mean?
OUTPUT: "entities_text": [], "wikipedia_urls": []
INPUT: Who is the child of Ranavalona I's husband?
OUTPUT: "entities_text": ["Ranavalona I"], "wikipedia_urls": ["https://en.wikipedia.org/wiki/Ranavalona_I"]
INPUT: What periodical literature does Delta Air Lines use as a moutpiece?
OUTPUT: "entities_text": ["periodical literature", "Delta Air Lines"], "wikipedia_urls": ["https://en.wikipedia.org/wiki/Periodical_literature", "https://en.wikipedia.org/wiki/Delta_Air_Lines"]
INPUT: What is award received of Hans Krebs where point in time is 1966-0-0?
OUTPUT: "entities_text": ["Hans Krebs"], "wikipedia_urls": ["https://en.wikipedia.org/wiki/Hans_Krebs_(biochemist)"]""",
        (
            "english",
            "simpleqs",
        ): """INPUT: How do plants grow?
OUTPUT: "entities_text": [], "wikipedia_urls": []
INPUT: what movie is produced by warner bros.
OUTPUT: "entities_text": ["warner bros."], "wikipedia_urls": ["https://en.wikipedia.org/wiki/Warner_Bros."]
INPUT: what is the gender of james hendry?
OUTPUT: "entities_text": ["james hendry"], "wikipedia_urls": ["https://en.wikipedia.org/wiki/James_Hendry_(obstetrician)"]""",
        (
            "english",
            "webqsp",
        ): """INPUT: what does the letters eu stand for?
OUTPUT: "entities_text": [], "wikipedia_urls": []
INPUT: what country is the grand bahama island in?
OUTPUT: "entities_text": ["grand bahama"], "wikipedia_urls": ["https://en.wikipedia.org/wiki/Grand_Bahama"]
INPUT: what character did john noble play in lord of the rings?
OUTPUT: "entities_text": ["john noble", "lord of the rings"], "wikipedia_urls": ["https://en.wikipedia.org/wiki/John_Noble", "https://en.wikipedia.org/wiki/The_Lord_of_the_Rings:_The_Two_Towers"]
INPUT: what city is the state capital of washington?
OUTPUT: "entities_text": ["washington"], "wikipedia_urls": ["https://en.wikipedia.org/wiki/Washington_(state)"]""",
        (
            "japanese",
            "lcquad2",
        ): """入力: 移民ってどういう意味?
出力: "entities_text": [], "wikipedia_urls": []
入力: ガリンスタンの相物質の前提条件は何ですか?
出力: "entities_text": ["ガリンスタン"], "wikipedia_urls": ["https://ja.wikipedia.org/wiki/ガリンスタン"]
入力: ハンセン病の治療に必要な必須医薬品は何ですか?
出力: "entities_text": ["ハンセン病", "必須医薬品"], "wikipedia_urls": ["https://ja.wikipedia.org/wiki/ハンセン病", "https://ja.wikipedia.org/wiki/必須医薬品"]
入力: ポルックスの地形的分離が 0.7 に等しいというのは本当ですか?
出力: "entities_text": ["ポルックス"], "wikipedia_urls": ["https://ja.wikipedia.org/wiki/ポッルチェ"]""",
        (
            "japanese",
            "simpleqs",
        ): """入力: 植物はどのように成長しますか?
出力: "entities_text": [], "wikipedia_urls": []
入力: ワーナー・ブラザースが製作する映画.
出力: "entities_text": ["ワーナー・ブラザース"], "wikipedia_urls": ["https://ja.wikipedia.org/wiki/ワーナー・ブラザース"]
入力: ヒューロン郡にある都市は何ですか
出力: "entities_text": ["ヒューロン郡"], "wikipedia_urls": ["https://ja.wikipedia.org/wiki/ヒューロン郡_(オハイオ州)"]""",
        (
            "japanese",
            "webqsp",
        ): """入力: euの文字は何の略ですか?
出力: "entities_text": [], "wikipedia_urls": []
入力: グランドバハマ島はどこの国?
出力: "entities_text": ["グランドバハマ島"], "wikipedia_urls": ["https://ja.wikipedia.org/wiki/グランド・バハマ島"]
入力: ロード・オブ・ザ・リングでジョン・ノーブルが演じた役は?
出力: "entities_text": ["ロード・オブ・ザ・リング", "ジョン・ノーブル"], "wikipedia_urls": ["https://ja.wikipedia.org/wiki/ロード・オブ・ザ・リング/二つの塔", "https://ja.wikipedia.org/wiki/ジョン・ノーブル"]
入力: ワシントン州の州都は何市?
出力: "entities_text": ["ワシントン州"], "wikipedia_urls": ["https://ja.wikipedia.org/wiki/ワシントン州"]""",
    }

    return responses.get((language, dataset), "No data available for the given language and dataset combination.")
