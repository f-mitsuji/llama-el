from pipeline.data_reader import read_correct_wikidata_ids, read_predicted_wikidata_ids


def calculate_evaluation_metrics(correct_ids, predicted_ids):
    metrics = {"precision": [], "recall": [], "f1": []}

    for true_ids, predicted_ids_for_line in zip(correct_ids, predicted_ids):
        true_positive = len(set(predicted_ids_for_line) & set(true_ids))
        false_positive = len(set(predicted_ids_for_line) - set(true_ids))

        if not true_ids and not predicted_ids_for_line:
            true_positive = 1
            false_positive = 0

        precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0
        recall = true_positive / len(true_ids) if len(true_ids) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        metrics["precision"].append(precision)
        metrics["recall"].append(recall)
        metrics["f1"].append(f1)

    total_lines = len(correct_ids)
    average_metrics = {key: sum(values) / total_lines for key, values in metrics.items() if total_lines > 0}

    return average_metrics.get("precision", 0), average_metrics.get("recall", 0), average_metrics.get("f1", 0)


def evaluate_model_prediction(model, dataset):
    correct_wikidata_file_path = f"datasets/test_datasets/{dataset}_test.json"
    predicted_wikidata_file_path = f"result/{dataset}/{model}/wikidata_id.json"

    correct_wikidata_ids = read_correct_wikidata_ids(correct_wikidata_file_path)
    predicted_wikidata_ids = read_predicted_wikidata_ids(predicted_wikidata_file_path)

    precision, recall, f1 = calculate_evaluation_metrics(correct_wikidata_ids, predicted_wikidata_ids)

    print_results(precision, recall, f1)


def print_results(precision, recall, f1):
    print("\n結果:")
    print(f"適合率: {precision:.3f}")
    print(f"再現率: {recall:.3f}")
    print(f"F値: {f1:.3f}")
