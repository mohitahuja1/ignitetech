"""
Say, the questions are divided into 4 categories based on their respective difficulties.
The test will start with a random question from 2nd level(mid-level). 
Then based on the whether the student has correctly answered the question, next question will be selected.
If the student answers a set number of correctly from the pool of questions at that particular level, 
he proceeds on to next level or falls one level down. 

During the test, the following must be displayed-
1.The detailed solution after the student provides an answer.
2.Time to solve the question.
3. The percentage progress at each level.

The detailed analysis of the test must include:
1.The concepts in which the student has made repetitive mistakes and thus, 
the link to the study material of the particular concept.
2. The concepts which takes the most time.
3.Total correct answer percentage and average total time for each question.

There is also one more suggestion, the adaptive learning model can choose the next question 
also based on the time taken to solve the previous question.
q
"""

# Import required libraries

import random
from collections import defaultdict
import pandas as pd
from .models import QuestionBank
from .models import UserQuestionScore
from .models import Profile
from .models import Test
from django.db.models import Max
from django.db.models import Min
from django.db.models import Count
from django.db.models import Sum


# Create class LearningNew

class LearningNew:

    def __init__(self):

        pass

    #@staticmethod
    def random_q(self, query_set):

        count = query_set.all().count()
        random_index = random.randint(0, count - 1)
        return query_set.all()[random_index]

    #@staticmethod
    def c_average(self, ele, n):
        ele[0] = float(float(float(ele[0] * ele[1]) + n) / float(ele[1] + 1))
        ele[1] = ele[1] + 1

    #@staticmethod
    def weak_concepts_fn(self, request):

        test = Test.objects.get(id=request.session['test_id'])

        # join data sets

        query_set = UserQuestionScore.objects.select_related('question').\
            values('user', 'test', 'attempt', 'correct', 'time_taken', 'question',
                   'question__level','question__correct_time').filter(user=request.user, test=test)

        # roll up data sets

        temp1 = query_set.values('question__level').annotate(other_time=Sum('question__correct_time')).\
            order_by('question__level')

        other_time = []

        for e in temp1:

            if e['question__level'] >= 0:
                other_time.append(e['other_time'])

        temp2 = query_set.values('question__level').annotate(time_taken=Sum('time_taken')). \
            order_by('question__level')

        time_taken = []

        for e in temp2:

            if e['question__level'] >= 0:
                time_taken.append(e['time_taken'])

        levels = []

        for e in range(request.session['distinct_levels']):

            levels.append(e+1)

        d1 = {'level': levels, 'other_time': other_time, 'time_taken': time_taken}

        index = [i for i in range(request.session['distinct_levels'])]

        df = pd.DataFrame(data=d1, index=index)

        df['attempts'] = request.session['attempts']

        df['corrects'] = request.session['corrects']

        #df['time_per_attempt'] = 0

        df['other_time_per_attempt'] = 0

        df['time_per_attempt'] = 0

        df['accuracy'] = 0

        df['time_per_attempt'][df['attempts'] != 0] = df['time_taken'] / df['attempts']

        df['other_time_per_attempt'][df['attempts'] != 0] = df['other_time'] / df['attempts']

        df['accuracy'][df['attempts'] != 0] = df['corrects'] / df['attempts']

        del df['time_taken']
        del df['other_time']
        del df['other_time_per_attempt']

        df['concept'] = ['Sample Space', 'Compound Events', 'Outcomes', 'Theoretical Probability',
                                 'Sampling Without Replacement', 'Dependent Events']

        df2 = df[['level', 'concept', 'attempts', 'corrects', 'accuracy', 'time_per_attempt']]

        with pd.option_context('display.max_colwidth', -1):
            result = df2.to_html(escape=False, index=False, float_format=lambda x: '%10.2f' % x,
                                 formatters=
                                 {'concept': '<a href = "javascript:void(0)" class="concept">{:}</a>'.format,
                                  # 'concept': '<a href = "#" onclick = "rev(this)">{:}</a>'.format,
                                  'accuracy': '{:,.0%}'.format, 'time_per_attempt': '{:,.3} sec'.format})
        return result

    #@staticmethod
    def create_session_vars(self, request):

        request.session['distinct_levels'] = QuestionBank.objects.values('level').filter(level__gt=-1).\
            distinct().count()

        temp1 = QuestionBank.objects.all().values('level').annotate(total=Count('question')).order_by('level')

        temp2 = []

        for t in temp1:

            if t['level'] >= 0:

                temp2.append(t['total'])

        request.session['questions'] = temp2

        request.session['attempts'] = [0] * request.session['distinct_levels']

        request.session['corrects'] = [0] * request.session['distinct_levels']

        # create a level cleared variable which takes the following values:
        # 1 if there are questions remaining in the level
        # 2 if questions completed with at least one correct answer
        # 3 if questions completed with no correct answer

        request.session['level_cleared'] = [0] * request.session['distinct_levels']


    #@staticmethod
    def get_next_level(self, request, curr_level, is_correct):

        if is_correct == 1:

            for i in range(curr_level+1, request.session['distinct_levels']):

                if request.session['level_cleared'][i] <= 1:
                    return i

                elif request.session['level_cleared'][i] == 2:
                    continue

                elif request.session['level_cleared'][i] == 3:
                    return 0

        elif is_correct == 0:

            for i in range(curr_level-1, -1, -1):

                if request.session['level_cleared'][i] <= 1:
                    return i

                elif request.session['level_cleared'][i] == 2:
                    continue

                elif request.session['level_cleared'][i] == 3:
                    continue

        return 0

    def learn(self, questionid, request, t, is_correct):

        if questionid == -1:

            user_level = Profile.objects.get(user=request.user).user_level

            if user_level == 1:
                level = QuestionBank.objects.all().aggregate(Min('level'))['level__min']
                query_set = QuestionBank.objects.filter(level=level)
                nq = self.random_q(query_set)

            elif user_level == 2:
                level = QuestionBank.objects.all().aggregate(Max('level'))['level__max']/2
                query_set = QuestionBank.objects.filter(level=level)
                nq = self.random_q(query_set)

            elif user_level == 3:
                level = QuestionBank.objects.all().aggregate(Max('level'))['level__max']
                query_set = QuestionBank.objects.filter(level=level)
                nq = self.random_q(query_set)

            result = []

            self.create_session_vars(request)

        else:

            question = QuestionBank.objects.get(id=questionid)
            curr_level = question.level

            user_metric = [question.pct_users, question.total_users]
            time_metric = [question.correct_time, question.correct_users]

            if is_correct == 1:

                self.c_average(user_metric, 0)
                request.session['attempts'][curr_level] += 1
                request.session['corrects'][curr_level] += 1

            elif is_correct == 0:

                self.c_average(time_metric, t)
                self.c_average(user_metric, 1)
                request.session['attempts'][curr_level] += 1

            question.pct_users = user_metric[0]
            question.total_users = user_metric[1]
            question.correct_time = time_metric[0]
            question.correct_users = time_metric[1]
            question.save()
            question.save()

            # update level cleared variable

            if request.session['attempts'][curr_level] < request.session['questions'][curr_level]:
                request.session['level_cleared'][curr_level] = 1

            elif request.session['attempts'][curr_level] == request.session['questions'][curr_level] \
                and request.session['corrects'][curr_level] > 0:
                request.session['level_cleared'][curr_level] = 2

            elif request.session['attempts'][curr_level] == request.session['questions'][curr_level] \
                    and request.session['corrects'][curr_level] == 0:
                request.session['level_cleared'][curr_level] = 3

            if is_correct == 1:

                if curr_level == request.session['distinct_levels']:

                    return -2, self.weak_concepts_fn(request)

                else:

                    next_level = self.get_next_level(request, curr_level, is_correct)

            elif is_correct == 0:

                if curr_level == 1:

                    return -2, self.weak_concepts_fn(request)

                else:

                    next_level = self.get_next_level(request, curr_level, is_correct)

            if next_level == 0:

                return -2, self.weak_concepts_fn(request)

            query_set = QuestionBank.objects.filter(userquestionscore__attempt=0, level=next_level)

            nq = self.random_q(query_set)

            result = None

        return nq, result


class Learning:

    # Initialize functions and variables

    def __init__(self, levels):

        # Create list of concepts

        self.concepts = [
            'General-Counting-',
            'General-Addition-',
            'General-Multiplication-',
            'General-Subtraction-',
            'General-Division-',
            'General-Comparing Numbers-',
            'Time-Days of week',
            'Time-Seasons of year',
            'Time-Read a Calendar',
            'Time-Months of year',
            'Time-AM or PM',
            'Time-No. of Days(Month)',
            'Time-Elapsed Time',
            '2D Shapes-Sides',
            '2D Shapes-vertices',
            '2D Shapes-angles',
            '2D Shapes-regular and irregular Polygons',
            '2D Shapes-Classification of triangles and quad',
            '2D Shapes-Lines and line Segments',
            '2D Shapes-Parallel and Perpendicular Lines',
            '2D Shapes-Parts of Circle',
            '3D Shapes-names',
            '3D Shapes-vertices',
            '3D Shapes-Edges',
            '3D Shapes-Faces',
            'Estimation and Rounding -',
            'Money-Coin Values',
            'Money-Making Changes',
            'Patterns-Repeating patterns',
            'Patterns-Growing Patterns',
            'Geometry-2D, 3D figures',
            'Geometry-Polygon',
            'Geometry-Reflection and translation',
            'Geometry-Symmetry',
            'Geometry-Perimeter',
            'Geometry-Area',
            'Geometry-Volume',
            'Geometry-Understanding Shapes',
            'Geometry-Constructions',
            'Geometry-mid-point',
            'Geometry-angle bisector',
            'Geometry-perpendicular lines',
            'Geometry-Types of triangles and properties',
            'Mesurement-units of measurement',
            'Mesurement-Compare size, mass and capacity',
            'Basic Properties-Addition,Sub,Mul and Div',
            'Basic Properties-paranthesis',
            'Basic Properties-Distributive',
            'Division Facts-',
            'Probablity-more,less or equally likely events',
            'Probablity-certain,probable,unlikely and impossible',
            'Probablity-Permutation and Combination',
            'Probablity-make predictions',
            'Probablity-compound events',
            'Probablity-Theoretical Probablity',
            'Probablity-mutually exclusive',
            'Probablity-simple events',
            'Number Sense-Even or Odd',
            'Number Sense-Number Line',
            'Number Sense-Metric Units(Conversion)',
            'Data and Graphs-Bar Graph',
            'Data and Graphs-Line plots',
            'Data and Graphs-Frequency Charts',
            'Data and Graphs-Histograms',
            'Data and Graphs-Venn Diagrams',
            'Data and Graphs-Stem and Leaf Ploats',
            'Fractions-Simple Fractions',
            'Fractions-Compound Fractions',
            'Fractions-Mixed fractions',
            'Fractions-Add and Subtract Fractions',
            'Decimals-Decimals to fractions',
            'Decimals-Add,Sub ,Mul ,Div of decimals',
            'Geometry-Lines of Symmetry',
            'Geometry-Rotational Symmetry',
            'Whole Numbers-',
            'Roman Numbers-',
            'Integers-Number Line',
            'Integers-Operations with Integers',
            'Number Theory-Divisblity Rules',
            'Number Theory-Prime Numbers',
            'Number Theory-Prime Factorisation',
            'Number Theory-HCF',
            'Number Theory-LCM',
            'Number Theory-Scientific Notation',
            'Exponents and Roots-',
            'Ratios-',
            'Rates -',
            'Proportions-',
            'Percentages-',
            '2D Shapes-Complementry angles',
            '2D Shapes-Supplementary Angles',
            '2D Shapes-Triangle Prop',
            '2D Shapes-Quad Prop',
            '2D Shapes-Adjacent angles',
            'Pytagoras Theorem-',
            'Rational Numbers-',
            'Statsitics-Mean',
            'Statsitics-Median ',
            'Statsitics-Mode ',
            'Statsitics-Range',
            'Coordinate Planes-',
            'Logic-or ',
            'Logic-and ',
            'Logic-not',
            'Logic-At least/ at most /or more / or less',
            'Probablity-Complementry events',
            'Probablity-Sample Space grid',
            'Probablity-Sample Space tree',
            'Data and Graphs-Table of Outcomes',
            'Probablity-Independent Events',
            'Probablity-Dependent Events',
            'Probablity-Sampling without replacement',
            'Probablity-Laws of Probablity',
            'Probablity-Conditional Probablity',
            'General-Roll a dice',
            'General-Flip a coin',
            'None'
        ]

        # Create graph that tells us the prerequisite concepts for each concept

        self.concepts_graph = {
            0: [],
            1: [0],
            2: [1],
            3: [0],
            4: [1, 3],
            5: [0],
            6: [0],
            7: [],
            8: [0],
            9: [8],
            10: [0],
            11: [0],
            12: [1, 3],
            13: [0],
            14: [0],
            15: [0],
            16: [5, 31],
            17: [13, 15, 16],
            18: [5],
            19: [15],
            20: [15, 18],
            21: [13, 15],
            22: [14],
            23: [13, 15],
            24: [13, 15],
            25: [5],
            26: [0],
            27: [1, 3],
            28: [0, 1, 2, 3, 4],
            29: [0, 1, 2, 3, 4],
            30: [13, 14, 15, 16, 17],
            31: [13, 14, 15],
            32: [2, 15, 19],
            33: [5, 15, 14, 13],
            34: [1, 2, 13, 22, 23],
            35: [1, 2, 13, 22, 23, 24],
            36: [1, 2, 13, 22, 23, 24],
            37: [17],
            38: [0, 13, 14, 15, 18, 19, 20],
            39: [4, 18, 19],
            40: [4, 15, 18],
            41: [4, 15, 18],
            42: [13, 15, 16],
            43: [0, 1, 2, 3, 4, 5],
            44: [0, 1, 2, 3, 4, 5],
            45: [0, 1, 2, 3, 4, 5],
            46: [0, 1, 2, 3, 4, 5],
            47: [1, 2],
            48: [0, 1, 2, 3, 4, 5],
            49: [0, 5],
            50: [0, 5],
            51: [0, 2, 3, 5],
            52: [49, 50, 51],
            53: [0, 2, 4, 5, 51, 49],
            54: [0, 2, 4, 5, 51, 49],
            55: [0, 49, 50, 54],
            56: [0, 1, 49, 50],
            57: [4],
            58: [0, 1],
            59: [0, 1, 2, 3, 4, 5],
            60: [0, 1, 4],
            61: [0, 1, 4, 58],
            62: [0, 1, 4, 58],
            63: [0, 1, 4, 58, 60],
            64: [0, 1, 4, 58, 20],
            65: [0, 1, 4, 58],
            66: [0, 1, 2, 3, 4],
            67: [0, 1, 2, 3, 4, 66],
            68: [0, 1, 2, 3, 4, 67],
            69: [0, 1, 2, 3, 4, 67, 68],
            70: [0, 1, 2, 3, 4, 67],
            71: [0, 1, 2, 3, 4, 70],
            72: [32, 33],
            73: [15, 72],
            74: [1, 2, 3, 4, 5],
            75: [74],
            76: [0, 1, 58],
            77: [74],
            78: [1, 2, 3, 4],
            79: [1, 2, 3, 4, 78],
            80: [79],
            81: [80],
            82: [80],
            83: [1, 2, 3, 4, 25, 84],
            84: [1, 2, 3, 4],
            85: [1, 2, 3, 4],
            86: [1, 2, 3, 4],
            87: [1, 2, 3, 4],
            88: [1, 2, 3, 4, 85],
            89: [1, 15],
            90: [1, 15],
            91: [13, 15, 16],
            92: [13, 15, 16],
            93: [1, 15],
            94: [91, 84],
            95: [67],
            96: [1, 2],
            97: [1, 2, 5],
            98: [5],
            99: [1, 3],
            100: [76],
            101: [0, 1],
            102: [0, 1],
            103: [0, 1, 2],
            104: [0, 1],
            105: [0, 3, 54],
            106: [0, 101, 102],
            107: [0, 101, 102],
            108: [0, 5],
            109: [54, 0, 51, 53],
            110: [0, 51, 54, 53],
            111: [54, 0],
            112: [64, 1, 3, 101, 102, 103],
            113: [112, 64, 4],
            114: [0, 5, 54],
            115: [0, 5, 54],
            116: []
        }

        # k = number of keys in the graph

        k = len(self.concepts_graph)

        # Create a k X k zeroes matrix

        temp = [[0 for x in xrange(k)] for y in xrange(k)]

        def change(key):
            temp[key][0] = 1
            temp[key][key] = 1
            values = self.concepts_graph[key]
            for y in values:
                temp[key][y] = 1
                change(y)

        # Execute function on all concepts

        for key in self.concepts_graph:
            change(key)

        # Initialize concept difficulty vector with all zeroes

        self.con_diff = [0] * len(self.concepts_graph)

        # Add number of pre requisites for each concept, which is the difficulty score

        c = 0
        for e in temp:
            self.con_diff[c] = sum(e)
            c += 1

        # Concepts related to each question

        self.q_graph = {
            0: [54],
            1: [54],
            2: [54, 69, 109, 111],
            3: [54, 115],
            4: [54, 115],
            5: [54, 107, 115],
            6: [54, 107, 115],
            7: [53, 54, 55, 69, 107, 109, 115],
            8: [54, 55, 109, 110, 111],
            9: [54, 55, 105, 109, 110, 111],
            10: [54],
            11: [54, 64],
            12: [54, 64, 69],
            13: [55],
            14: [55, 112],
            15: [109, 113],
            16: [109, 112, 113]
        }

        # Calculate the overall difficulty of a question =
        # sum of difficulty level of its prerequisite concepts

        q_diff = [0] * len(self.q_graph)

        for x in xrange(len(self.q_graph.keys())):
            for y in self.q_graph[self.q_graph.keys()[x]]:
                q_diff[x] = q_diff[x] + self.con_diff[y]

        self.q_diff = q_diff

        # Create levels of questions based on their difficulty
        # Levels will be input to function
        # q_level will be list of levels corresponding to q_graph

        self.q_level = [0] * len(self.q_graph)

        # list l stores scores for each concept based on questions solved by the student

        self.l = [100] * len(self.concepts)

        # Build list q_level that specifies level of each question

        self.total_levels = levels

        # keep track of the questions displayed/answered

        self.answered_q = [0] * len(self.q_level)

        # start with median level

        self.create_groups()

        # levels checked

        self.l_checked = [0] * (self.total_levels + 1)

        # total questions corresponding to each level

        self.total_questions = [self.q_level.count(i) for i in range(self.total_levels)]

        # attempted questions corresponding to each level

        self.attempted = [0] * (self.total_levels)

        # total incorrect questions answered corresponding to each level

        self.wrong = [0] * (self.total_levels)

        # create score for each concept based on accuracy within each level

        self.con_score = defaultdict(dict)

        # time taken per question

        self.que_time = [0] * len(self.q_level)

        self.que_other_time = [0] * len(self.q_level)

        self.tm = [[0,0] for _ in xrange(len(self.q_level))]

        # Each row in the matrix corresponds to a concept.
        # The function below will change those columns to 1 that correspond to a
        # prerequisite concept. It will recursively do this for all pre requisites.

    # Create groups based on levels

    def create_groups(self):
        c = []
        size = len(self.q_diff)
        for x in xrange(size):
            c.append((self.q_diff[x], x))
        c.sort()
        k = (size / float(self.total_levels))
        for x in xrange(size):
            self.q_level[c[x][1]] = int(x / k)

    # Return random question based on specified difficulty level
    # Current level is input and takes integer values

    def random_q(self):
        indices = [i for i, j in enumerate(self.q_level) if j == self.curr_level]
        r = random.randint(0, len(indices) - 1)
        return indices[r]

    # Return total number of questions corresponding to a level

    def total_q(self):
        return sum([1 for x in self.q_level if x == self.curr_level])

    # Only decimal (not fractional) submissions will be allowed
    # Create function to round off to two decimal places

    def is_correct(self, x, y):
        return int(abs(float(x) - float(y)) <= 0.01)

    # Create function that performs below operation on an (average, n) pair

    def c_average(self, ele, n):
        ele[0] = float(float(float(ele[0] * ele[1]) + n) / float(ele[1] + 1))
        ele[1] = ele[1] + 1

    # if the answer is correct, increase the score of the prerequisite concepts by 1

    def correct_ans(self, que, t, user_metric, time_metric):

        for x in self.q_graph[que]:
            # 100 is just an initial value to test whether the student has answered any
            # question which has this pre-requisite concept
            if (self.l[x] == 100):
                self.l[x] = 1
            else:
                self.l[x] = self.l[x] + 1
                # update concept score
            if x in self.con_score[self.q_level[que]]:
                self.con_score[self.q_level[que]][x] += self.con_diff[x]
            else:
                self.con_score[self.q_level[que]][x] = self.con_diff[x]
        self.que_time[que] = t
        self.c_average(time_metric, t)
        self.c_average(user_metric, 1)
        self.que_other_time[que] = time_metric[0]

        return user_metric, time_metric

    # if the answer is wrong, decrease the score of the prerequisite concepts by 1

    def wrong_ans(self, que, t, user_metric, time_metric):

        for x in self.q_graph[que]:
            if (self.l[x] == 100):
                self.l[x] = -1
            else:
                self.l[x] = self.l[x] - 1
                # update concept_score
            if x in self.con_score[self.q_level[que]]:
                self.con_score[self.q_level[que]][x] -= self.con_diff[x]
            else:
                self.con_score[self.q_level[que]][x] = self.con_diff[x]
        self.que_time[que] = t
        self.c_average(user_metric, 0)
        self.que_other_time[que] = time_metric[0]

        return user_metric, time_metric


    def weak_concepts_fn(self):


        d1 = {'level': self.q_level, 'total_time': self.que_time, 'other_time': self.que_other_time}
        index = [i for i in range(len(self.q_level))]
        df1 = pd.DataFrame(data=d1, index=index)

        d2 = df1.groupby('level').sum()

        index2 = [i for i in range(len(d2))]

        df2 = pd.DataFrame(data=d2, index=index2)

        df2['attempted'] = self.attempted

        df2['wrong'] = self.wrong

        df2['time_per_attempt'] = 0

        df2['other_time_per_attempt'] = 0

        df2['accuracy'] = 0

        df2['time_per_attempt'][df2['attempted'] != 0] = df2['total_time'] / df2['attempted']

        df2['other_time_per_attempt'][df2['attempted'] != 0] = df2['other_time'] / df2['attempted']

        df2['accuracy'][df2['attempted'] != 0] = (df2['attempted'] - df2['wrong']) / df2['attempted']

        del df2['wrong']
        del df2['total_time']
        del df2['other_time']

        out1 = []
        for e in index2:
            if self.con_score[e]:
                out1.append(min(self.con_score[e], key=self.con_score[e].get))
            else:
                out1.append(-1)

        out2 = []
        for e in out1:
            out2.append(self.concepts[e])

        df2['weak_concept'] = out2

        return df2.to_html()

    # function to get the next question

    def next_que(self, level):
        mval = -1
        nq = -1
        n = [-1] * len(self.q_graph.keys())
        v = [0] * len(self.q_graph.keys())

        # graph.keys() = question numbers
        for x in xrange(len(self.q_graph.keys())):
            n[x] = self.q_graph.keys()[x]

            # Check if the question is of required level
            if (self.q_level[x] == level and self.answered_q[n[x]] == 0):
                for y in self.q_graph[n[x]]:
                    if (self.l[y] == 100):
                        v[x] = v[x] + 5
                    elif (self.l[y] < 100 and self.l[y] > 0):
                        v[x] = v[x]
                    elif (self.l[y] <= 0 and self.l[y] > -3):
                        v[x] = v[x] + 10
                    elif (self.l[y] <= -3):
                        v[x] = v[x] - 100

                mval = max(v[x], mval)
                if (mval == v[x]):
                    nq = n[x]

        # In case concept priority above can't decide nq, put any remaining question in level as nq

        for x in xrange(len(self.q_graph.keys())):
            if nq == -1 and self.answered_q[n[x]] == 0:
                nq = n[x]

        return nq

    def learn(self, question_id, t, user_metric, time_metric, is_correct):

        if question_id == -1:

            self.curr_level = self.total_levels / 2

            nq = self.random_q()

            result = []

        else:

            self.curr_level = self.q_level[question_id]

            self.attempted[self.curr_level] = self.attempted[self.curr_level] + 1

            self.answered_q[question_id] = 1

            # if answer is incorrect

            if is_correct == 0:

                user_metric, time_metric = self.wrong_ans(question_id, t, user_metric, time_metric)
                self.wrong[self.curr_level] = self.wrong[self.curr_level] + 1

            # if answer is correct

            if is_correct == 1:
                user_metric, time_metric = self.correct_ans(question_id, t, user_metric, time_metric)

            # if attempts > 75% of total questions and accuracy < 50% in level, go up a level

            if (self.attempted[self.curr_level] / float(self.total_questions[self.curr_level])) >= 0.75 and \
                                (self.wrong[self.curr_level] / float(self.attempted[self.curr_level])) >= 0.5:
                self.curr_level = self.curr_level - 1
                if (self.l_checked[self.curr_level] == 0):
                    self.l_checked[self.curr_level] = 1
                else:
                    return -2, self.weak_concepts_fn(), user_metric, time_metric

            # if attempts > 75% of total questions and accuracy > 50% in level, go up a level

            if (self.attempted[self.curr_level] / float(self.total_questions[self.curr_level])) >= 0.75 and \
                            (self.wrong[self.curr_level] / float(self.attempted[self.curr_level])) < 0.5:
                self.curr_level = self.curr_level + 1
                if (self.l_checked[self.curr_level] == 0):
                    self.l_checked[self.curr_level] = 1
                else:
                    return -2, self.weak_concepts_fn(), user_metric, time_metric

            # if all levels cleared, show analysis

            if (self.curr_level >= self.total_levels):
                return -2, self.weak_concepts_fn(), user_metric, time_metric

            # if no level cleared, show analysis

            if (self.curr_level < 0):
                return -2, self.weak_concepts_fn(), user_metric, time_metric

            nq = self.next_que(self.curr_level)

            result = self.weak_concepts_fn()

        return nq, result, user_metric, time_metric
