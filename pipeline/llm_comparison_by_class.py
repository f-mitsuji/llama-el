from pipeline.data_reader import read_predicted_wikidata_ids


def analyze_el_accuracy_by_class(
    correct_ids: list[list[str]] | list[str],
    predicted_ids: list[list[str]],
    data: list[dict[str, list[str]]],
) -> tuple[dict[str, int], dict[str, int]]:
    """英語WebQSPデータセットのTP, FNをクラスで分析する関数

    Args:
        correct_ids (list[list[str]] | list[str]): データセットの正解Wikidata ID
        predicted_ids (list[list[str]]): LLMによる予測Wikidata ID
        data (list[dict[str, list[str]]]): データセットのデータ（entity_classesキーのため）

    Returns:
        tuple[dict[str, int], dict[str, int]]: TP, FNそれぞれのクラス分析の結果
    """
    true_positive_classes_count: dict[str, int] = {}
    false_negative_classes_count: dict[str, int] = {}

    for i, (true_ids, predicted_ids_for_line) in enumerate(zip(correct_ids, predicted_ids)):

        true_positive = set(predicted_ids_for_line) & set(true_ids)
        false_negatives = set(true_ids) - set(predicted_ids_for_line)

        for entity_id in true_positive:
            if entity_id in data[i]["entities"]:
                entity_class = data[i]["entity_classes"][data[i]["entities"].index(entity_id)]
                true_positive_classes_count[entity_class] = true_positive_classes_count.get(entity_class, 0) + 1
            else:
                true_positive_classes_count["Unknown"] = true_positive_classes_count.get("Unknown", 0) + 1

        for entity_id in false_negatives:
            if entity_id in data[i]["entities"]:
                entity_class = data[i]["entity_classes"][data[i]["entities"].index(entity_id)]
                false_negative_classes_count[entity_class] = false_negative_classes_count.get(entity_class, 0) + 1
            else:
                false_negative_classes_count["Unknown"] = false_negative_classes_count.get("Unknown", 0) + 1

    return true_positive_classes_count, false_negative_classes_count


def compare_llm_by_class(
    correct_ids: list[list[str]] | list[str],
    llama2_ids: list[list[str]],
    dataset: str,
    data: list[dict[str, list[str]]],
):
    gpt4_ids = read_predicted_wikidata_ids(f"result/{dataset}/gpt-4/wikidata_id.json")
    true_positive_class_gpt4, false_negative_class_gpt4 = analyze_el_accuracy_by_class(correct_ids, gpt4_ids, data)
    true_positive_class_llama2, false_negative_class_llama2 = analyze_el_accuracy_by_class(
        correct_ids, llama2_ids, data
    )

    print(f"Llama2 FP Class: {true_positive_class_llama2}")
    print(f"Llama2 FN Class: {false_negative_class_llama2}")
    print(f"GPT-4 TP Class: {true_positive_class_gpt4}")
    print(f"GPT-4 FN Class: {false_negative_class_gpt4}")
