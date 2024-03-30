import json
import time
from pathlib import Path
from urllib.parse import quote

from pipeline.data_reader import read_json_file
from SPARQLWrapper import JSON, SPARQLWrapper

WIKIDATA_SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"


def get_wikidata_ids(url: str, language: str) -> list[str]:
    """Use Wikidata's SPARQL endpoint to convert Wikipedia URL to Wikidata ID

    Args:
        url (str): Wikipedia URL

    Returns:
        list[str]: Wikidata ID or empty list
    """
    try:
        if language == "japanese":
            url = quote(url, safe=":/")
        sparql_wikidata = SPARQLWrapper(WIKIDATA_SPARQL_ENDPOINT, returnFormat="json")
        query = f"""
        PREFIX schema: <http://schema.org/>
        SELECT * WHERE {{
            <{url}> schema:about ?item .
        }}
        """
        sparql_wikidata.setQuery(query)
        sparql_wikidata.setReturnFormat(JSON)
        results = sparql_wikidata.query().convert()
        result_bindings = results["results"]["bindings"]
        time.sleep(1)  # 1クライアント60秒間に60秒の処理時間許容

        return [binding["item"]["value"].split("/")[-1] for binding in result_bindings]

    except Exception as e:  # noqa: BLE001
        print(f"Error fetching Wikidata IDs for URL {url}: {e}")
        time.sleep(10)

        return []


def process_data_point(data_point: dict[str, list[str]], language: str) -> dict[str, int | str | list[str]]:
    entities_text = data_point.get("entities_text", [])
    wikipedia_urls = data_point.get("wikipedia_urls", [])
    labels = [label.strip() for label in entities_text]
    wikidata_ids_for_line: list[str] = []

    for url in wikipedia_urls:
        wikidata_ids = get_wikidata_ids(url, language)
        wikidata_ids_for_line.extend(wikidata_ids or [""])
    # index = data_point.get("id", "")
    # print(f"index: {index}, id: {wikidata_ids_for_line}")

    return {"id": data_point.get("id", ""), "entities_text": labels, "wikidata_ids": wikidata_ids_for_line}


def convert_wikipedia_url_to_wikidata_id(model: str, dataset: str, language: str) -> None:
    # input_file_path = f"result/{dataset}/{model}/wikipedia_url_test.json"
    # output_file_path = f"result/{dataset}/{model}/wikidata_id_test.json"
    input_file_path = f"result/{dataset}/{model}/wikipedia_url.json"
    output_file_path = Path(f"result/{dataset}/{model}/wikidata_id.json")

    entity_url_data = read_json_file(input_file_path)
    data_list = [process_data_point(data_point, language) for data_point in entity_url_data]

    with output_file_path.open(mode="w", encoding="UTF-8") as f:
        json.dump(data_list, f, ensure_ascii=False)
