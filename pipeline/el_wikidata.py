import json
import time

from SPARQLWrapper import JSON, SPARQLWrapper

from pipeline.data_reader import read_json_file


def get_wikidata_ids(url):  # urlに空白が含まれているとエラー起きる対策後でする
    try:
        sparql_wikidata = SPARQLWrapper("https://query.wikidata.org/sparql", returnFormat="json")
        query = """
        PREFIX schema: <http://schema.org/>
        SELECT * WHERE {{
            <{0}> schema:about ?item .
        }}
        """.format(
            url
        )
        sparql_wikidata.setQuery(query)
        sparql_wikidata.setReturnFormat(JSON)
        results = sparql_wikidata.query().convert()
        result_bindings = results["results"]["bindings"]
        time.sleep(1)  # 1クライアント60秒間に60秒の処理時間許容
        return [binding["item"]["value"].split("/")[-1] for binding in result_bindings]
    except Exception as e:
        print(f"Error fetching Wikidata IDs for URL {url}: {e}")
        time.sleep(10)
        return []


def process_data_point(data_point):
    entities_text = data_point.get("entities_text", [])
    wikipedia_urls = data_point.get("wikipedia_urls", [])
    labels = [label.strip() for label in entities_text]
    wikidata_ids_for_line = []

    for url in wikipedia_urls:
        wikidata_ids = get_wikidata_ids(url)
        wikidata_ids_for_line.extend(wikidata_ids or [""])

    return {"id": data_point.get("id", ""), "entities_text": labels, "wikidata_ids": wikidata_ids_for_line}
    # return {"index": data_point.get("index", ""), "entities_text": labels, "wikidata_ids": wikidata_ids_for_line}


def wikipedia_url_to_wikidata_id(model, dataset):
    # input_file_path = f"result/{dataset}/{model}/wikipedia_url_test.json"
    # output_file_path = f"result/{dataset}/{model}/wikidata_id_test.json"
    input_file_path = f"result/{dataset}/{model}/wikipedia_url.json"
    output_file_path = f"result/{dataset}/{model}/wikidata_id.json"
    entity_url_data = read_json_file(input_file_path)

    data_list = [process_data_point(data_point) for data_point in entity_url_data]

    with open(output_file_path, "w", encoding="UTF-8") as output_file:
        json.dump(data_list, output_file, ensure_ascii=False, indent=2)
