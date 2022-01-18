import csv

# import data csv already read

# transformations

# generate false labeled data

# save
import random
from typing import List
import math
import string
import numpy as np
from nltk.corpus import wordnet


class DataSetGenerator:
    def __init__(self, sourceDateSet,configs:dict={"number_negative_data_same_category": 300, "number_negative_data_different_category": 100,
                          "number_positive_data_same_category": 400}):
        self.source_dataset = []
        i=0
        with open(sourceDateSet) as source:
            for row in csv.reader(source, delimiter=','):
                if i==0:
                    print(row)
                    i+=1
                self.source_dataset.append(row)
        self.organize_source()
        # print(self.source_dataset)
        # open and read files
        # initialize configs
        self.number_negative_data_same_category = configs.get("number_negative_data_same_category")
        self.number_negative_data_different_category = configs.get("number_negative_data_different_category")
        self.number_positive_data_same_category = configs.get("number_positive_data_same_category")
        self.synonym_switching_rate = 1
        self.typos_injection_rate = 0.9
        self.punctuation_insetion_rate = 0.3
        self.punctuation = '!\'#$%&\'()*+, -./:;<=>?@[\]^_`{|}~'

    def organize_source(self):
        """
        remove spaces in source data
        :return:
        """
        for i, data in enumerate(self.source_dataset):
            self.source_dataset[i][0] = " ".join(data[0].split())

    def create(self, destDataSet):  # adi
        """
        creating datatset of two sentences and a positive(1) or negative(0) label
        :param destDataSet:
        :return: dataset
        """
        positive_data = self.transforms()
        # transforms
        negative_data = self.create_negative_data()
        all_data = positive_data + negative_data
        random.shuffle(all_data)
        with open(destDataSet, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            for row in all_data:
                spamwriter.writerow(row)
        # zero labeled using sentences from the same catgory
        # zero labeld no from the same catgory

    def create_negative_data(self) -> List[List]:
        """
        create negative data by different samples from the same category and from different categories
        :return: all negative samples list
        """
        all_negative_samples = []
        category_data_dict = {}
        for data in self.source_dataset:
            if category_data_dict.get(data[1]) is None:
                category_data_dict[data[1]] = [data[0]]
            else:
                category_data_dict[data[1]] += [data[0]]
        samples = random.sample(self.source_dataset, self.number_negative_data_same_category)
        for sample in samples:
            negative_sample = random.sample(category_data_dict[sample[1]], 1)
            all_negative_samples.append([sample[0], negative_sample[0], 0])
        samples = random.sample(self.source_dataset, self.number_negative_data_different_category)
        for sample in samples:
            negative_sample = random.sample(self.source_dataset, 1)
            all_negative_samples.append([sample[0], negative_sample[0][0], 0])
        assert len(
            all_negative_samples) == self.number_negative_data_different_category + self.number_negative_data_same_category
        return all_negative_samples

    def transforms(self) -> List:  # efrat
        """
        create positive data by slightly changing sentences.
        :return: all positive samples list
        """
        all_positive_samples = []
        category_data_dict = {}
        for data in self.source_dataset:
            if category_data_dict.get(data[1]) is None:
                category_data_dict[data[1]] = [data[0]]
            else:
                category_data_dict[data[1]] += [data[0]]
        samples = random.sample(self.source_dataset, self.number_positive_data_same_category)
        for sample in samples:
            new_sentence = sample[0]
            if random.random() < self.synonym_switching_rate:
                new_sentence = self.switchingSynonym(new_sentence)
            if random.random() < self.typos_injection_rate:
                new_sentence = self.injectTypos(new_sentence)
            if random.random() < self.punctuation_insetion_rate:
                new_sentence = self.punctuationInsertion(new_sentence)
            all_positive_samples.append([sample[0], new_sentence, 1])
        return all_positive_samples

    def injectTypos(self, sentence):  # efrat
        """
        Randomly adds typos to the given sentence.
        :param sentence:
        :return: sentence with typos
        """

        def typo(x):
            if random.random() < 0.01:  # insertion right
                return random.choice(string.ascii_letters + string.digits) + x
            if random.random() < 0.01:  # insertion left
                return x + random.choice(string.ascii_letters + string.digits)
            if random.random() < 0.01:  # replace
                return random.choice(string.ascii_letters + string.digits)
            if random.random() < 0.01:  # deletion
                return ""
            return x

        return ''.join(map(typo, sentence))


    def switchingSynonym(self, sentence: str,number_words_to_change:int=3) -> str:  # adi
        """
        finding the first word in the shuffle list that can be switched to a similar word and switch it.
        :param sentence:
        :return: sentence with switch
        """
        sentance_list = sentence.split(" ")
        shuffle_index = list(range(len(sentance_list)))
        random.shuffle(shuffle_index)
        number_words_changed=0
        for i in shuffle_index:
            if number_words_changed==number_words_to_change:
                break
            word_synonyms=[]
            for syn in wordnet.synsets(sentance_list[i]):
                for lm in syn.lemmas():
                    if lm.name()!=sentance_list[i]:
                        word_synonyms.append(lm.name())
            if len(word_synonyms)>0:
                sentance_list[i]=word_synonyms[0]
                number_words_changed+=1
        return " ".join(sentance_list)


    def punctuationInsertion(self, sentence):  # efrat
        """
        Randomly adds punctuation to the given sentence. Prefers adding punctuation next to spaces.
        :param sentence:
        :return: sentence with punctuation insertions
        """

        def randPunctuation():
            return random.choice(string.punctuation)

        return ''.join(map(lambda x: (randPunctuation() + x if random.random() < 0.5 else x + randPunctuation()) if (
                    (x.isspace() and random.random() < 0.05) or random.random() < 0.005) else x, sentence))
