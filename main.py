import argparse

from pipeline.el_wikipedia import entity_wikipedia_url_extractor
from pipeline.el_wikidata import wikipedia_url_to_wikidata_id
from pipeline.eval import calculate_metrics


def main():
    parser = argparse.ArgumentParser(
        description='Arguments of input for task functions'
    )

    parser.add_argument(
        '-t',
        '--task',
        type=str,
        default='url',
        choices=['url', 'id', 'eval'],
        help='Task'
    )

    parser.add_argument(
        '-m',
        '--model',
        type=str,
        default='llama-2-70b',
        choices=['llama-2-7b', 'llama-2-13b', 'llama-2-70b'],
        help='Model'
    )

    parser.add_argument(
        '-d',
        '--dataset',
        type=str,
        default='webqsp',
        choices=['laquad2', 'simpleqs', 'webqsp'],
        help='Dataset'
    )

    args = parser.parse_args()

    if args.task == 'url':
        entity_wikipedia_url_extractor(args.model, args.dataset)
    elif args.task == 'id':
        wikipedia_url_to_wikidata_id()
    elif args.task == 'eval':
        calculate_metrics()
    else:
        raise NotImplementedError(
            "Please select your task from ['url', 'id', 'eval'].")


if __name__ == "__main__":
    main()
