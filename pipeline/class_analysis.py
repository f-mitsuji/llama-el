def analyze_el_accuracy_by_class(
    correct_ids: list[list[str]] | list[str],
    predicted_ids: list[list[str]],
    dataset: str,
    data: list[dict[str, list[str]]],
) -> None:
    true_positive_classes_count: dict[str, int] = {}
    false_negative_classes_count: dict[str, int] = {}

    for i, (true_ids, predicted_ids_for_line) in enumerate(zip(correct_ids, predicted_ids)):

        if dataset == "simpleqs":
            true_ids = [true_ids]  # type: ignore

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

    print(f"true_positive_classes: {true_positive_classes_count}")
    print(f"false_negative_classes: {false_negative_classes_count}")
