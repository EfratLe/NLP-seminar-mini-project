import csv

# import data csv already read

# transformations

# generate false labeled data

# save
import random
from typing import List

import numpy as np


class DataSetGenerator:
    def __init__(self, sourceDateSet, similarWordsDataSet, configs={}):
        self.source_dataset = []
        with open(sourceDateSet) as source:
            for row in csv.reader(source, delimiter=','):
                self.source_dataset.append(row)
        self.similarity_data = []
        with open(similarWordsDataSet) as source:
            for row in csv.reader(source, delimiter=','):
                self.similarity_data.append((row[0], row[1]))
        self.similarity_data_row_0 = [data[0] for data in self.similarity_data]
        self.similarity_data_row_1 = [data[1] for data in self.similarity_data]
        # print(self.source_dataset)

        # open and read files
        # initialize configs
        self.number_negative_data_same_category = 200
        self.number_negative_data_different_category = 200

        self.punctuation = '!\'#$%&\'()*+, -./:;<=>?@[\]^_`{|}~'
        pass

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
        print(all_data)
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
        # for sentence:
        # randomly select words for switching

        return []

    def injectTypos(self, word):  # efrat
        # return string
        pass

    def switchingSynonym(self, sentence: str) -> str:  # adi
        """
        finding the first word in the shuffle list that can be switched to a similar word and switch it.
        :param sentence:
        :return: sentence with switch
        """
        sentance_list = sentence.split(" ")
        shuffle_index = list(range(len(sentance_list)))
        random.shuffle(shuffle_index)
        for i in shuffle_index:
            index = self.similarity_data_row_0.index(sentance_list[i]) if sentance_list[
                                                                              i] in self.similarity_data_row_0 else -1
            if index != -1:
                sentance_list[i] = self.similarity_data_row_1[index]
                break
            index = self.similarity_data_row_1.index(sentance_list[i]) if sentance_list[
                                                                              i] in self.similarity_data_row_1 else -1
            if index != -1:
                sentance_list[i] = self.similarity_data_row_0[index]
                break
        print(sentance_list)
        return " ".join(sentance_list)

    def panctuatuionInsertion(self, sentence):  # efrat
        pass
