# NLP-seminar-mini-project
Near duplication is a widespread phenomenon on the Web and, therefore, an issue in NLP datasets. This project addresses the classification problem of near-duplicate sentences by generating new datasets and providing codebase for dataset generation. We offer classical distance-based solution to near-duplication detection as part of our codebase. 

This is a mini project done as part of a seminar in NLP (236817) at Technion.

# installation
To install the project in an existing conda environment, run the following lines of code:
```
conda install -c conda-forge --file requirements.txt
pip install sentence-transformers==2.1.0
```

# running the code
run the following command line to generate the dataset, using test.csv as the base dataset :
```
python main.py --create_dataset --test_dataset
```

The optional flags to run the code with:

```--create_dataset``` - Create the dataset and save it in the same directory under the name "generated-dataset-demo.csv".

```-p``` - A path to the base dataset csv. if not used the genreated dataset would be based on test.csv.

```--test_dataset``` - Test the performance of the similarity methods on the dataset

![image](https://user-images.githubusercontent.com/29407344/151696869-798ee3f9-1787-4cb6-a8c3-57fc7c720806.png)

# configurations

The DataSetGenerator class contains the dataset generation code and configuration. It receives the based dataset location and a config dictionary. The config dictionary should state the number of negative examples to generate of the same category, different categories, and positive examples. The sentences are chosen randomly. synonym_switching_rate determines the synonym switching rate - the percentage of positive samples with synonym switching (max number of switching in a sentence is currently 1). typos_injection_rate and punctuation_insertion_rate determine the percentage of positive examples with these transformations.
