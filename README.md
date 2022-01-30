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

#configurations
