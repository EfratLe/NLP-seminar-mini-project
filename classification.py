from typing import List, Tuple

import numpy as np
from sklearn.model_selection import StratifiedKFold
from sentance_similarity import BertEmbed, StringDistance


class Classification():

    def __init__(self, similarityClass: StringDistance, all_dataX, all_dataY, method_check="accuracy"):
        self.all_x = all_dataX
        self.all_y = all_dataY
        self.similarity_class = similarityClass
        self.best_threshold = -1
        self.n_splits = 5
        self.thresholds = [0.5, .6, .7, .8, .9]
        if method_check == "accuracy":
            self.score_method = self.accuracy
        else:
            self.score_method = self.f_score

    def get_data_from_index(self, all_x: List, all_y: List, indexes_list: List[int]) -> Tuple[List, List]:
        """
        seperate x and y
        :param all_x:
        :param all_y:
        :param indexes_list:
        :return:
        """
        x = [all_x[index] for index in indexes_list]
        y = [all_y[index] for index in indexes_list]
        return x, y

    def accuracy(self, y_our: List, y_true: List) -> float:
        """
        accuracy calculation
        :param y_our:
        :param y_true:
        :return:
        """
        acc = 0
        for i, y in enumerate(y_our):
            if y == y_true[i]:
                acc += 1
        return acc / len(y_our)

    def f_score(self, y_our: List, y_true: List) -> float:
        """
        f-score calculation
        :param y_our:
        :param y_true:
        :return:
        """
        tp = 0
        fp = 0
        fn = 0
        for i, y in enumerate(y_our):
            if y == y_true[i]:
                if y == "1":
                    tp += 1
                else:
                    assert y == y_true[i]=="0"
                    fn += 1
            if y != y_true[i] and y == "1":
                fp += 1
        return tp / (tp + 0.5 * (fp + fn))

    def train(self, x_train: List[Tuple], y_train: List):
        """
        find best threshold using the training data
        :param x_train:
        :param y_train:
        :return:
        """
        best_threshold = -1
        best_threshold_accuracy = 0
        for threshold in self.thresholds:
            y_pred = []
            for x in x_train:
                similarity = self.similarity_class.getSimilarity(x[0], x[1])
                if similarity > threshold:
                    y_pred.append("1")
                else:
                    y_pred.append("0")
            acc = self.score_method(y_pred, y_train)
            if acc > best_threshold_accuracy:
                best_threshold_accuracy = acc
                best_threshold = threshold
        self.best_threshold = best_threshold

    def test(self, x_test: List[Tuple], y_test: List) -> float:
        """
        return accuracy on test
        :param x_test:
        :param y_test:
        :return:
        """
        y_pred = []
        for x in x_test:
            similarity = self.similarity_class.getSimilarity(x[0], x[1])
            if similarity > self.best_threshold:
                y_pred.append("1")
            else:
                y_pred.append("0")
        return self.score_method(y_test, y_pred)

    def run_classification(self):
        """
        run classification few times using kfold
        :return:
        """
        accL = []
        accT = []
        skf = StratifiedKFold(n_splits=self.n_splits)
        for train_index, test_index in skf.split(self.all_x, self.all_y):
            x_t, y_t = self.get_data_from_index(self.all_x, self.all_y, train_index)
            x_test, y_test = self.get_data_from_index(self.all_x, self.all_y, test_index)
            self.train(x_t, y_t)
            accL.append(self.test(x_test, y_test))
            accT.append(self.test(x_t, y_t))
            # print(f"the best threshold is {self.best_threshold}")
        average_score_of_option = np.array(accL).sum(axis=0) / len(accL)
        print(f"the average accuracy over {self.n_splits} iteration on TEST is {round(average_score_of_option,3)}")
        average_score_of_option = np.array(accT).sum(axis=0) / len(accL)
        print(f"the average accuracy over {self.n_splits} iteration on TRAIN is {round(average_score_of_option,3)}")
