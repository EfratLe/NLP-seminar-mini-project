# NLP-seminar-mini-project
To install in an existing conda environment, run the following lines of code:
```
conda install -c conda-forge --file requirements.txt
pip install sentence-transformers==2.1.0
```

To run the code, run the line:
```
python main.py --create_dataset -p --test_dataset --f_score
```

The optional flags to run the code with:

```--create_dataset``` -  will create the dataset and will save it in the same directory under the name "generated-dataset-demo.csv"

```-p``` - give a path to the csv to use (the first column needs to be the sentences and the second column the classification value).
if not used will create data set using test.csv

```--test_dataset``` - will test the performance of the similarity methods on the dataset

```--f_score``` - will test the performance using f-score. If not adding it the performance method will be accuracy.
