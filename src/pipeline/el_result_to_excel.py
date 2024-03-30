import pandas as pd
from pipeline.data_reader import (
    read_dataset_file,
    read_predicted_wikidata_ids,
    read_predicted_wikipedia_urls,
)


def compare_predictions(data, correct_ids, gpt4_ids, gpt4_urls, llama2_ids, llama2_urls, dataset, language):
    common_missed, gpt4_only_missed, llama2_only_missed = [], [], []

    for i, (entry, correct_id, gpt4_id, llama2_id, gpt4_url, llama2_url) in enumerate(
        zip(data, correct_ids, gpt4_ids, llama2_ids, gpt4_urls, llama2_urls, strict=False), 1
    ):
        key_for_question = "question"
        if language != "japanese" and dataset == "webqsp":
            key_for_question = "utterance"

        missed_id_gpt4 = set(correct_id) - set(gpt4_id)
        missed_id_llama2 = set(correct_id) - set(llama2_id)

        if missed_id_gpt4 and missed_id_llama2:
            common_missed.append(
                (i, entry[key_for_question], correct_id, missed_id_gpt4, gpt4_url, missed_id_llama2, llama2_url),
            )
        elif missed_id_gpt4:
            gpt4_only_missed.append((i, entry[key_for_question], correct_id, missed_id_gpt4, gpt4_url))
        elif missed_id_llama2:
            llama2_only_missed.append((i, entry[key_for_question], correct_id, missed_id_llama2, llama2_url))

    return common_missed, gpt4_only_missed, llama2_only_missed


def save_comparison_results(common_missed, gpt4_only_missed, llama2_only_missed, output_path):
    df_common = pd.DataFrame(
        common_missed,
        columns=[
            "Question Number",
            "Question",
            "Correct IDs",
            "Missed IDs (GPT-4)",
            "Wikipedia URLs (GPT-4)",
            "Missed IDs (Llama 2)",
            "Wikipedia URLs (Llama 2)",
        ],
    )
    df_gpt4_only = pd.DataFrame(
        gpt4_only_missed,
        columns=["Question Number", "Question", "Correct IDs", "Missed IDs (GPT-4)", "Wikipedia URLs (GPT-4)"],
    )
    df_llama2_only = pd.DataFrame(
        llama2_only_missed,
        columns=["Question Number", "Question", "Correct IDs", "Missed IDs (Llama 2)", "Wikipedia URLs (Llama 2)"],
    )

    with pd.ExcelWriter(output_path) as writer:
        df_common.to_excel(writer, sheet_name="Common Missed", index=False)
        df_gpt4_only.to_excel(writer, sheet_name="GPT-4 Only Missed", index=False)
        df_llama2_only.to_excel(writer, sheet_name="Llama 2 Only Missed", index=False)


def compare_llm_predictions(correct_ids, llama2_ids, model, dataset, dataset_file_path, language):
    data = read_dataset_file(dataset_file_path)
    output_excel_path = f"result/{dataset}/{model}/gpt4-{model}-comparison.xlsx"
    gpt4_ids = read_predicted_wikidata_ids(f"result/{dataset}/gpt-4/wikidata_id.json")
    gpt4_urls = read_predicted_wikipedia_urls(f"result/{dataset}/gpt-4/wikipedia_url.json")
    llama2_urls = read_predicted_wikipedia_urls(f"result/{dataset}/{model}/wikipedia_url.json")

    common_missed, gpt4_only_missed, llama2_only_missed = compare_predictions(
        data,
        correct_ids,
        gpt4_ids,
        gpt4_urls,
        llama2_ids,
        llama2_urls,
        dataset,
        language,
    )
    save_comparison_results(common_missed, gpt4_only_missed, llama2_only_missed, output_excel_path)
