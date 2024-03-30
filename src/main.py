import argparse

from pipeline.el_wikipedia import entity_wikipedia_url_extractor
from pipeline.eval import evaluate_model_prediction
from pipeline.wikipedia_url_to_wikidata_id import convert_wikipedia_url_to_wikidata_id


def main() -> None:
    parser = argparse.ArgumentParser(description="Arguments of input for task functions")

    parser.add_argument(
        "-t",
        "--task",
        type=str,
        choices=["url", "id", "eval"],
        help="Task",
    )

    parser.add_argument(
        "-m",
        "--model",
        type=str,
        choices=["llama-2-7b", "llama-2-13b", "llama-2-70b", "Swallow-7b", "Swallow-13b"],
        help="Model",
    )

    parser.add_argument(
        "-d",
        "--dataset",
        type=str,
        choices=["lcquad2", "simpleqs", "webqsp"],
        help="Dataset",
    )

    parser.add_argument(
        "-l",
        "--language",
        type=str,
        choices=["english", "japanese"],
        help="Language",
    )

    args = parser.parse_args()

    if args.task == "url":
        entity_wikipedia_url_extractor(args.model, args.dataset, args.language)
    elif args.task == "id":
        convert_wikipedia_url_to_wikidata_id(args.model, args.dataset, args.language)
    elif args.task == "eval":
        evaluate_model_prediction(args.model, args.dataset, args.language)
    else:
        error_msg = "Please select your task from ['url', 'id', 'eval']."
        raise NotImplementedError(error_msg)


if __name__ == "__main__":
    main()
