from typing import List

from sentence_transformers import SentenceTransformer
from numpy import dot
from numpy.linalg import norm


class StringDistance():
    def __init__(self):
        pass

    def getSimilarity(self, sentence1: str, sentence2: str) -> float:
        return 1

    def get_name(self) -> str:
        return "similarityDistance"


class editSimilarity(StringDistance):
    def __init__(self):
        super(editSimilarity, self).__init__()

    def get_name(self) -> str:
        return "editSimilarity"

    def edit_distance(self, s1, s2):
        if len(s1) > len(s2):
            s1, s2 = s2, s1

        distances = range(len(s1) + 1)
        for i2, c2 in enumerate(s2):
            distances_ = [i2 + 1]
            for i1, c1 in enumerate(s1):
                if c1 == c2:
                    distances_.append(distances[i1])
                else:
                    distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
            distances = distances_
        return distances[-1]

    def getSimilarity(self, sentence1: str, sentence2: str) -> float:
        edit_distance = self.edit_distance(sentence1, sentence2)
        return 1 - (edit_distance / (min(len(sentence1), len(sentence2))))


class jaccardSimilarity(StringDistance):
    def __init__(self):
        super(jaccardSimilarity, self).__init__()

    def get_name(self) -> str:
        return "jaccardSimilarity"

    def jaccard_similarity(self, list1: List[str], list2: List[str]) -> float:
        intersection = len(list(set(list1).intersection(list2)))
        union = (len(set(list1)) + len(set(list2))) - intersection
        return float(intersection) / union

    def getSimilarity(self, sentence1: str, sentence2: str) -> float:
        list1 = list(sentence1)
        list2 = list(sentence2)
        return self.jaccard_similarity(list1, list2)


class overlapSimilarity(StringDistance):
    def __init__(self):
        super(overlapSimilarity, self).__init__()

    def overlap(self, list1: List[str], list2: List[str]) -> float:
        intersection = len(list(set(list1).intersection(list2)))
        return intersection / min(len(list1), len(list2))

    def getSimilarity(self, sentence1: str, sentence2: str) -> float:
        list1 = list(sentence1)
        list2 = list(sentence2)
        return self.overlap(list1, list2)

    def get_name(self) -> str:
        return "overlapSimilarity"


class BertEmbed(StringDistance):
    def __init__(self):
        super(BertEmbed, self).__init__()
        self.word_dist_embedding = {}
        self.model = SentenceTransformer('all-mpnet-base-v2')

    def get_name(self) -> str:
        return "sentanceBest"

    def getSimilarity(self, sentence1: str, sentence2: str) -> float:
        embed1 = self.get_bert_embed(sentence1)
        embed2 = self.get_bert_embed(sentence2)

        return dot(embed1, embed2) / (norm(embed1) * norm(embed2))

    def get_bert_embed(self, word: str):
        embed = self.word_dist_embedding.get(word)
        if embed is not None:
            return embed
        embed = self.create_embedding(word)
        self.word_dist_embedding[word] = embed
        return embed

    def create_embedding(self, word: str):
        sentence_embeddings = self.model.encode(word)
        return sentence_embeddings
