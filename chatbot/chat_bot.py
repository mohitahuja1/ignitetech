# -*- coding: UTF-8 -*-
import numpy
from sklearn.feature_extraction.text import CountVectorizer # countvectorizer creates tokens for each data set
import numpy.linalg as LA  # importing the linear algebra module
from .models import QnaRepository
from .models import QuestionBank
from adaptive_learning.models import UserConceptScore


class ChatBot:

    def __init__(self):

        self.id_list = QnaRepository.objects.values_list('id', flat=True)
        self.question_list = QnaRepository.objects.values_list('question', flat=True)
        self.concept_list = QnaRepository.objects.values_list('concept', flat=True)
        self.doubt_list = QnaRepository.objects.values_list('doubt', flat=True)
        self.answer_list = QnaRepository.objects.values_list('answer', flat=True)

    def get_dic(self, q_id):

        dic = dict()

        for i in range(len(self.id_list)):
            if (QuestionBank.objects.get(pk=self.question_list[i]).question == "None") or \
                    (self.question_list[i] == int(q_id)):
                dic[self.doubt_list[i]] = self.answer_list[i]

        return dic

    def model(self, train_dataset, new_data):

        new = [new_data]
        ques_list = list(train_dataset.keys())
        vectorizer, trainvectorizerarray = self.train_func(ques_list)
        new_test = vectorizer.transform(new).toarray()  # creating a token for the new input data
        cx = lambda a, b: round(numpy.inner(a, b) / (LA.norm(a) * LA.norm(b)), 3)

        for testV in new_test:  # selecting the new token that was created for the input question
            cos = 0.0
            ans = ''

            for n, vector in enumerate(trainvectorizerarray):  # selecting the first token
                cosine = cx(vector, testV)  # finding the cosine similarity between selected token and new token

                if cosine > cos:
                    cos = cosine
                    a = ques_list[n]
                    ans = train_dataset[a]

            if ans == '':
                return ('Sorry! I couldn\'t understand that. Please be more specific.')
            else:
                return ans

    @staticmethod
    def train_func(train):

        stopwords = ['the', 'is', 'are', 'were', 'a', 'an', 'was', 'has', 'had', 'have', 'to', 'do', 'of', 'on',
                     'my', 'any', 'be', 'by']  # the words that should be ignored by countvectoriser
        vectorizer = CountVectorizer(stop_words=stopwords)  # adding the words list to countvectoriser
        train_set = train # creating the training set
        trainvectorizerarray = vectorizer.fit_transform(train_set).toarray()
        # creating tokens from the training set. This is a 2D array
        return vectorizer,trainvectorizerarray

    def main_bot(self, question_id, user_query, user):  # question_id - string, user_query

        question_dict = self.get_dic(question_id)
        answer = self.model(question_dict, user_query)
        concept = QnaRepository.objects.filter(answer=answer)[0].concept
        userconcept = UserConceptScore.objects.get(user=user, concept=concept)
        userconcept.asked += 1
        userconcept.save()

        return answer

