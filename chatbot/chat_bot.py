# -*- coding: UTF-8 -*-
import numpy
from sklearn.feature_extraction.text import CountVectorizer # countvectorizer creates tokens for each data set
import numpy.linalg as LA  # importing the linear algebra module
from .models import QnaRepository
from .models import QuestionBank
from adaptive_learning.models import UserConceptScore
from adaptive_learning.models import Concept
from django.db.models import Min
from django.db.models import Max


class ChatBot:

    def __init__(self):

        pass

    def get_dic(self, q_id):

        dic = dict()

        if int(q_id) >= 0:

            qna_set = QnaRepository.objects.filter(question__in=[QuestionBank.objects.get(id=q_id),
                                                                 QuestionBank.objects.get(question="None")])

        else:

            qna_set = QnaRepository.objects.filter(question=QuestionBank.objects.get(question="None"))

        for i in range(len(qna_set)):
            dic[str(qna_set[i].doubt)] = str(qna_set[i].answer)

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
                return "Sorry! I couldn't understand. Try asking differently or chat with a teacher."
            else:
                return ans

    @staticmethod
    def train_func(train):

        stopwords = ['the', 'is', 'are', 'were', 'a', 'an', 'was', 'has', 'had', 'have', 'to', 'do', 'of', 'on',
                     'my', 'any', 'be', 'by']
        vectorizer = CountVectorizer(stop_words=stopwords)
        train_set = train
        trainvectorizerarray = vectorizer.fit_transform(train_set).toarray()
        return vectorizer,trainvectorizerarray

    def main_bot(self, question_id, user_query, request):

        question_dict = self.get_dic(question_id)
        answer = self.model(question_dict, user_query)

        if answer == "Sorry! I couldn't understand. Try asking differently or chat with a teacher.":
            return answer

        if int(question_id) < 0:
            return answer

        concept = QnaRepository.objects.filter(answer=answer)[0].concept
        userconcept = UserConceptScore.objects.get(user=request.user, concept=concept)
        userconcept.asked += 1
        userconcept.save()

        conlevel = Concept.objects.get(concept = concept).concept_level

        qna = QnaRepository.objects.select_related('concept'). \
            values('question', 'concept', 'doubt', 'concept__concept_level'). \
            filter(question=QuestionBank.objects.get(id=question_id))

        con = Concept.objects.prefetch_related('userconceptscore_set'). \
            filter(userconceptscore__user=request.user, userconceptscore__asked__lt=50)

        qna_ucs = qna.filter(concept__in=con)

        conlevelmax = qna_ucs.aggregate(Max('concept__concept_level'))['concept__concept_level__max']

        if conlevelmax is None:
            return answer

        for i in range(conlevel+1, conlevelmax+1):

            for j in range(len(qna_ucs)):

                if i == qna_ucs[j]['concept__concept_level']:

                    bot_suggestion = "<br><br>You can also ask:<br><br><a href='#' onclick='clickfunc(this)'>" +\
                                     qna_ucs[j]['doubt'] + "</a>"

                    answer += bot_suggestion

                    return answer

        bot_suggestion = "<br><br>You can also ask:<br><br>" + \
                         "Please tell me the <a href='#' onclick='clickfunc(this)'>solution</a>."

        answer += bot_suggestion

        return answer
