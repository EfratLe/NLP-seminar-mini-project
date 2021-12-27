from typing import List, Tuple

from DataSetGenerator import DataSetGenerator
import csv

from classification import Classification
from sentance_similarity import BertEmbed, jaccardSimilarity, editSimilarity,overlapSimilarity

# generator = DataSetGenerator("mini-project-sentences-dataset.csv"
#                              , "similar-related-pairs.csv")
# generator.create("generated-dataset-demo.csv")
#
# generator.switchingSynonym("50-year-old problem of biology solved by Artificial Intelligence")


similarityDistanceClasses=[BertEmbed(),jaccardSimilarity(),editSimilarity(),overlapSimilarity()]





def main():
    # create dataset
    generator = DataSetGenerator("mini-project-sentences-dataset.csv"
                                 , "similar-related-pairs.csv")
    generator.create("generated-dataset-demo.csv")

    # get data
    all_dataX, all_dataY = [], []
    with open("generated-dataset-demo.csv") as source:
        for row in csv.reader(source, delimiter=','):
            all_dataX.append((row[0], row[1]))
            all_dataY.append(row[2])

    # run classification
    for similarity in similarityDistanceClasses:
        print(f"running classification using {similarity.get_name()}")
        classification=Classification(similarity,all_dataX,all_dataY)
        classification.run_classification()



if __name__ == "__main__":
    main()




#todo
# we need to find a better dataset
# we need to make the test harder maybe change more words...
# maybe need to find more ways other then accuracy to give score