import csv

#import data csv already read

#transformations

#generate false labeled data

#save


class DataSetGenerator:
    def __init__(self, sourceDateSet, similarWordsDataSet, configs ={}):
        self.source_dataset=[]
        with open(sourceDateSet) as source:
            for row in csv.reader(source, delimiter=','):
                self.source_dataset.append(row)
        print(self.source_dataset)

        #open and read files
        #initialize configs
        self.punctuation = '!\'#$%&\'()*+, -./:;<=>?@[\]^_`{|}~'
        pass

    def create(self,destDataSet): #adi
        #transforms
        #zero labeled using sentences from the same catgory
        #zero labeld no from the same catgory
        pass

    def transforms(self): #efrat
        #for sentence:
            #randomly select words for switching

        pass

    def injectTypos(self,word): #efrat
        #return string
        pass

    def switchingSynonym(self,sentence): #adi
        pass

    def panctuatuionInsertion(self, sentence): #efrat
        pass

