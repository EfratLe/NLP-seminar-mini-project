import argparse
from typing import List, Tuple

from DataSetGenerator import DataSetGenerator
import csv

from classification import Classification
from sentance_similarity import BertEmbed, jaccardSimilarity, editSimilarity, overlapSimilarity

similarityDistanceClasses = [BertEmbed(), jaccardSimilarity(), editSimilarity(), overlapSimilarity()]


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--create_dataset", action="store_true",
                        help="will create the dataset and will save it in the same directory under the name 'generated-dataset-demo.csv'")
    parser.add_argument("-p", "--dataset_path", required=False,
                        help="give a path to the csv to use (the first column needs to be the sentences and the second column the classification value).if not used will create data set using test.csv")
    parser.add_argument("--test_dataset", action="store_true",
                        help=" will test the performance of the similarity methods on the dataset")
    parser.add_argument("--f_score", action="store_true",
                        help="will test the performance using f-score. If not adding it the performance method will be accuracy.")
    return parser.parse_args()


def create_dataset(path="test.csv"):
    generator = DataSetGenerator(path)
    generator.create("generated-dataset-demo.csv")


def test_dataset(method="accuracy"):
    # get data
    all_dataX, all_dataY = [], []
    with open("generated-dataset-demo.csv") as source:
        for row in csv.reader(source, delimiter=','):
            all_dataX.append((row[0], row[1]))
            all_dataY.append(row[2])

    # run classification
    for similarity in similarityDistanceClasses:
        print(f"running classification using {similarity.get_name()}")
        classification = Classification(similarity, all_dataX, all_dataY, method)
        classification.run_classification()


def run_all(args):
    if args.create_dataset == True:
        if args.dataset_path != None:
            print(args.dataset_path)
            create_dataset(args.dataset_path)
        else:
            create_dataset()
    if args.test_dataset == True:
        method = "accuracy"
        if args.f_score == True:
            method = "f_score"
        test_dataset(method)


if __name__ == "__main__":
    args = parse_args()
    run_all(args)
