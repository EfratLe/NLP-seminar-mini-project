from DataSetGenerator import DataSetGenerator

generator = DataSetGenerator("mini-project-sentences-dataset.csv"
                             ,"similar-related-pairs.csv")
generator.create("generated-dataset-demo.csv")
