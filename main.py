import argparse

from pipeline.el_wikidata import wikipedia_url_to_wikidata_id
from pipeline.el_wikipedia import entity_wikipedia_url_extractor
from pipeline.eval import evaluate_model_prediction


def main():
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
        choices=["llama-2-7b", "llama-2-13b", "llama-2-70b", "Swallow-7b"],
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
        wikipedia_url_to_wikidata_id(args.model, args.dataset)
    elif args.task == "eval":
        evaluate_model_prediction(args.model, args.dataset, args.language)
    else:
        raise NotImplementedError("Please select your task from ['url', 'id', 'eval'].")


if __name__ == "__main__":
    main()
