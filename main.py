import argparse
from typing import List, Tuple

from DataSetGenerator import DataSetGenerator
import csv

from classification import Classification
from sentance_similarity import BertEmbed, jaccardSimilarity, editSimilarity, overlapSimilarity

# generator = DataSetGenerator("mini-project-sentences-dataset.csv"
#                              , "similar-related-pairs.csv")
# generator.create("generated-dataset-demo.csv")
#
# generator.switchingSynonym("50-year-old problem of biology solved by Artificial Intelligence")


similarityDistanceClasses = [BertEmbed(), jaccardSimilarity(), editSimilarity(), overlapSimilarity()]


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--create_dataset", action="store_true")
    parser.add_argument("--test_dataset", action="store_true")
    parser.add_argument("--f_score", action="store_true")
    return parser.parse_args()


def create_dataset():
    generator = DataSetGenerator("mini-project-sentences-dataset.csv")
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
        create_dataset()
    if args.test_dataset == True:
        method = "accuracy"
        if args.f_score == True:
            method = "f_score"
        test_dataset(method)


if __name__ == "__main__":
    args = parse_args()
    run_all(args)
    # main()

# todo
# we need to find a better dataset
# we need to make the test harder maybe change more words...
# maybe need to find more ways other then accuracy to give score
