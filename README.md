# NLP-seminar-mini-project
To install the project in an existing conda environment, run the following lines of code:
```
conda install -c conda-forge --file requirements.txt
pip install sentence-transformers==2.1.0
```

run the following command line to generate the dataset, using test.csv as the base dataset :
```
python main.py --create_dataset --test_dataset
```

The optional flags to run the code with:

```--create_dataset``` - Create the dataset and save it in the same directory under the name "generated-dataset-demo.csv".

```-p``` - A path to the base dataset csv. if not used the genreated dataset would be based on test.csv.

```--test_dataset``` - Test the performance of the similarity methods on the dataset
