# -*- coding: UTF-8 -*-
import numpy
import json
import os.path
import sys
from sklearn.feature_extraction.text import CountVectorizer # countvectoriser creats tokens for each data set
import numpy.linalg as LA #importing the linear algebra module

from .models import qna_repository

qid_list = qna_repository.objects.values_list('question_id',flat = True)

q_list = qna_repository.objects.values_list('q',flat = True)

a_list = qna_repository.objects.values_list('a',flat = True)

def get_dic(q_id):
    dic = dict()
    for i in range(len(qid_list)):
        if (qid_list[i] == -1) or (qid_list[i] == int(q_id)):
            dic[q_list[i]] = a_list[i]
    return dic

def model(train_dataset,new_data):

    new = [new_data]
    ques_list = list(train_dataset.keys())
    vectorizer, trainVectorizerArray = train_func(ques_list)
    new_test = vectorizer.transform(new).toarray()  # creating a token for the new input data
    cx = lambda a, b: round(numpy.inner(a, b) / (LA.norm(a) * LA.norm(b)), 3)

    for testV in new_test:  # selecting the new token that was created for the input question
        cos = 0.0
        ans = ''
        for n, vector in enumerate(trainVectorizerArray):  # selecting the first token
            cosine = cx(vector, testV)  # finding the cosine similarity between the selected token and the new token

            if cosine > cos:
                cos = cosine

                a = ques_list[n]
                ans = train_dataset[a]
        if ans == '':
            return ('Sorry! I couldn\'t understand that. Please be more specific.')
        else:
            return(ans)

def train_func(train):
    stopWords = ['the', 'is', 'are', 'were', 'a', 'an', 'was', 'has', 'had', 'have','to','do','of','on','my','any','be','by'] #the words that should be ignored by countvectoriser
    vectorizer = CountVectorizer(stop_words=stopWords)  # adding the words list to countvectoriser
    train_set = train # creating the training set
    trainVectorizerArray = vectorizer.fit_transform(train_set).toarray()  # creating tokens froms the trainng set, This is a 2D array
    return vectorizer,trainVectorizerArray

def main_bot(question_id, user_query):                  # question_id - string, user_query
    question_dict = get_dic(question_id)
    answer = model(question_dict, user_query)
    print answer
    return (answer)

