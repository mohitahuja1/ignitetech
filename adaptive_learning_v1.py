
# Import required libraries

import numpy as np
import math
import random
import time
#from prettytable import PrettyTable

# Create list of concepts

concepts=[
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
'General-Flip a coin'

]


# Create graph that tells us the prerequisite concepts for each concept

concepts_graph={
0:[],
1:[0],
2:[1],
3:[0],
4:[1,3],
5:[0],
6:[0],
7:[],
8:[0],
9:[8],
10:[0],
11:[0],
12:[1,3],
13:[0],
14:[0],
15:[0],
16:[5,31],
17:[13,15,16],
18:[5],
19:[15],
20:[15,18],
21:[13,15],
22:[14],
23:[13,15],
24:[13,15],
25:[5],
26:[0],
27:[1,3],
28:[0,1,2,3,4],
29:[0,1,2,3,4],
30:[13,14,15,16,17],
31:[13,14,15],
32:[2,15,19],
33:[5,15,14,13],
34:[1,2,13,22,23],
35:[1,2,13,22,23,24],
36:[1,2,13,22,23,24],
37:[17],
38:[0,13,14,15,18,19,20],
39:[4,18,19],
40:[4,15,18],
41:[4,15,18],
42:[13,15,16],
43:[0,1,2,3,4,5],
44:[0,1,2,3,4,5],
45:[0,1,2,3,4,5],
46:[0,1,2,3,4,5],
47:[1,2],
48:[0,1,2,3,4,5],
49:[0,5],
50:[0,5],
51:[0,2,3,5],
52:[49,50,51],
53:[0,2,4,5,51,49],
54:[0,2,4,5,51,49],
55:[0,49,50,54],
56:[0,1,49,50],
57:[4],
58:[0,1],
59:[0,1,2,3,4,5],
60:[0,1,4],
61:[0,1,4,58],
62:[0,1,4,58],
63:[0,1,4,58,60],
64:[0,1,4,58,20],
65:[0,1,4,58],
66:[0,1,2,3,4],
67:[0,1,2,3,4,66],
68:[0,1,2,3,4,67],
69:[0,1,2,3,4,67,68],
70:[0,1,2,3,4,67],
71:[0,1,2,3,4,70],
72:[32,33],
73:[15,72],
74:[1,2,3,4,5],
75:[74],
76:[0,1,58],
77:[74],
78:[1,2,3,4],
79:[1,2,3,4,78],
80:[79],
81:[80],
82:[80],
83:[1,2,3,4,25,84],
84:[1,2,3,4],
85:[1,2,3,4],
86:[1,2,3,4],
87:[1,2,3,4],
88:[1,2,3,4,85],
89:[1,15],
90:[1,15],
91:[13,15,16],
92:[13,15,16],
93:[1,15],
94:[91,84],
95:[67],
96:[1,2],
97:[1,2,5],
98:[5],
99:[1,3],
100:[76],
101:[0,1],
102:[0,1],
103:[0,1,2],
104:[0,1],
105:[0,3,54],
106:[0,101,102],
107:[0,101,102],
108:[0,5],
109:[54,0,51,53],
110:[0,51,54,53],
111:[54,0],
112:[64,1,3,101,102,103],
113:[112,64,4]
114:[0,5,54]
115:[0,5,54]
}

# k = number of keys in the graph

k = len(concepts_graph)

# Create a k X k zeroes matrix 

temp = [[0 for x in xrange(k)] for y in xrange(k)]

# Each row in the matrix corresponds to a concept.
# The function below will change those columns to 1 that correspond to a 
# prerequisite concept. It will recursively do this for all pre requisites.

def change(key):
    temp[key][0] = 1
    temp[key][key] = 1
    values = concepts_graph[key]
    for y in values:
        temp[key][y] = 1
        change(y)

# Execute function on all concepts

for key in concepts_graph:
        change(key)
        
# Initialize concept difficulty vector with all zeroes
        
con_diff=[0]*len(concepts_graph)

# Add number of pre requisites for each concept, which is the dificulty score

c = 0
for e in temp:
    con_diff[c] = sum(e)
    c += 1

    
# Sample questions

question=

[

'A box contains 4 red and 2 yellow tickets.What is the probablity that the first selected is red.',

'A box contains 4 red and 2 yellow tickets.If the first selected ticket is red, find the probablity that second selected ticket is also red',

'A box contains 4 red and 2 yellow tickets. Two tickets are randomly selected from the box one by one without replacement. Find the probability that both are red.',

'Two boxes each contain 6 petunia plants that are not yet flowering. Box A contains 2 plants that will have purple flowers and 4 plants that will have white flowers.Box B contains 5 plants that will have purple flowers and 1 plant that will have white flowers. A box is selected by tossing a coin, and one plant is removed at random from it. Determine the probablity of selecting box 1.',

'Two boxes each contain 6 petunia plants that are not yet flowering. Box A contains 2 plants that will have purple flowers and 4 plants that will have white flowers. Box B contains 5 plants that will have purple flowers and 1 plant that will have white flowers. A box is selected by tossing a coin, and one plant is removed at random from it.Determine the probablity of selecting box 2.',

'Two boxes each contain 6 petunia plants that are not yet flowering. Box A contains 2 plants that will have purple flowers and 4 plants that will have white flowers. Box B contains 5 plants that will have purple flowers and 1 plant that will have white flowers. A box is selected by tossing a coin, and one plant is removed at random from it.Detemine the probablity of selecting a purple flower if box 1 selected.',

'Two boxes each contain 6 petunia plants that are not yet flowering. Box A contains 2 plants that will have purple flowers and 4 plants that will have white flowers. Box B contains 5 plants that will have purple flowers and 1 plant that will have white flowers. A box is selected by tossing a coin, and one plant is removed at random from it.Detemine the probablity of selecting a purple flower if box 2 is selected.',

'Two boxes each contain 6 petunia plants that are not yet flowering. Box A contains 2 plants that will have purple flowers and 4 plants that will have white flowers. Box B contains 5 plants that will have purple flowers and 1 plant that will have white flowers. A box is selected by tossing a coin, and one plant is removed at random from it. Determine the probability that it will have purple flowers.',

'A bag contains 5 red and 3 blue marbles. Two marbles are drawn simultaneously from the bag. Detemine the probablity that no red balls are selected.',

'A bag contains 5 red and 3 blue marbles. Two marbles are drawn simultaneously from the bag.Determine the probability that at least one is red.',

'In a class of 30 students, 19 study Physics, 17 study Chemistry, and 15 study both of these subjects.Find the number of students who study at least one subject.',

'In a class of 30 students, 19 study Physics, 17 study Chemistry, and 15 study both of these subjects.Find the no. of students who study neither subject.',

'In a class of 30 students, 19 study Physics, 17 study Chemistry, and 15 study both of these subjects.Find probablity of student who study both subject.',

'In a class of 30 students, 19 study Physics, 17 study Chemistry, and 15 study both of these subjects.Find the probablity that student who study at least one subject.',

'In a class of 30 students, 19 study Physics, 17 study Chemistry, and 15 study both of these subjects.Find the probablity that students who study physics but not chemistry.',

'Suppose P(A) = 1/2, P(B) = 1/3 , and P(A U B) = p.What the P(A intersection B) if both are mutually exclusive.',

'Suppose P(A) = 1/2, P(B) = 1/3 , and P(A U B) = p. Find p if A and B are mutually exclusive.',

'Suppose P(A) = 1/2, P(B) = 1/3 , and P(A U B) = p.What the P(A intersection B) if both are independent.',

'Suppose P(A) = 1/2, P(B) = 1/3 , and P(A U B) = p.What the P(A intersection B) if both are independent.'

]

# List of answers
ans=

[
    '4/6',
    '3/5',
    '2/5',
    '1/2',
    '1/2',
    '2/6',
    '5/6',
    '7/12',
    '3/28',
    '25/28',
    '21',
    '9',
    '1/2',
    '21/30',
    '4/30',
    '0',
    '5/6',
    '1/6',
    '2/3'
    
]

# Concepts related to each question

q_graph={
    0:[0,1,4,54],
    1:[0,1,4,54],
    2:[0,1,4,54,109,69,111],
    3:[5,115,54],
    4:[5,115,54],
    5:[1,4,5,107,115,54],
    6:[1,4,5,107,115,54],
    7:[1,2,4,5,107,115,54,109,69,53,55],
    8:[],
    9:[],
    10:[],
    11:[],
    12:[],
    13:[],
    14:[],
    15:[],
    16:[],
    17:[],
    18:[],
    19:[]


    3:[1,54,64,69],
    4:[1,54,109,112,55]}

# Calculate the overall difficulty of a question = 
# sum of difficulty level of its prerequisite concepts

q_diff=[0]*len(q_graph)

for x in xrange(len(q_graph.keys())):
    for y in q_graph[q_graph.keys()[x]]:
        q_diff[x]=q_diff[x]+con_diff[y]
        
print q_diff           

import copy

# Create levels of questions based on their difficulty
# Levels will be input to function
# q_level will be list of levels corresponding to q_graph

q_level=[0]*len(q_graph)

def create_groups(levels):
    c=[]
    size = len(q_diff)
    for x in xrange(size):
        c.append((q_diff[x],x))
    c.sort()
    k= (size/float(levels))
    for x in xrange(size):
        q_level[c[x][1]]=int(x/k)

# Return random question based on specified difficulty level
# Current level is input and takes integer values

def random_q(curr_level):
    indices = [i for i, j in enumerate(q_level) if j == curr_level]
    r=random.randint(0,len(indices)-1)
    return indices[r]
    
# Return total number of questions corresponding to a level

def total_q(curr_level):
    return sum([1 for x in q_level if x == curr_level])

# Only decimal (not fractional) submissions will be allowed
# Create function to round off to two decimal places

def is_correct(x,y):
    return int(abs(x-y) <= 0.01)  
    
# Create function that performs below operation on an (average, n) pair

def c_average(ele,n):
    ele[0]=float(float(float(ele[0]*ele[1])+n)/float(ele[1]+1))
    ele[1]=ele[1]+1
        
# Create data structure to store time and user info for each question

time_metric =[[0,0] for _ in xrange(len(question))]
user_metric =[[0,0] for _ in xrange(len(question))]

    
# list l stores scores for each concept based on questions solved by the student
    
l=[100]*len(concepts)
    
# Build list q_level that specifies level of each question
    
total_levels=2
    
# keep track of the questions displayed/answered
    
answered_q=[0]*len(q_level) 
    
# define total no. of levels in test
    
curr_level=total_levels/2 
    
# total questions taken
    
total_que=0
    
# total incorrect questions answered
    
wrong=0
    
# start with median level    
    
create_groups(total_levels)

# levels checked    
    
l_checked=[0]*(total_levels+1)
    
# create score for each concept based on accuracy within each level
    
from collections import defaultdict

con_score = defaultdict(dict)

# time taken per question

que_time=[0]*len(question)

    
#if the answer is correct, increase the score of the prerequisite concepts by 1
def correct_ans(que,t):
    print ("Correct Answer")
    print("%s percent of %s users got this right" %(m_que_cavg[que][0]*100,m_que_cavg[que][1]))
    print("Time : %s" %t)
    print("Average time taken by users who got this right: %s" %m_que_tavg[que][0])
    for x in q_graph[que]:
        #100 is just an initial value to test whether the student has answered any
        #question which has this pre-requisite concept
        if(l[x]==100):
            l[x]=1
        else:
            l[x]=l[x]+1    
    # update concept score
        if x in con_score[q_level[que]]:
            con_score[q_level[que]][x] += con_diff[x]
        else:
            con_score[q_level[que]][x] = con_diff[x]
    que_time[que]=t
    c_average(m_que_tavg[que],t)
    c_average(m_que_cavg[que],1)
    
#if the answer is wrong, decrease the score of the prerequisite concepts by 5
def wrong_ans(que,t):
    print("Wrong Answer")
    print("%s percent of %s users got this right" %(m_que_cavg[que][0]*100,m_que_cavg[que][1]))
    print("Time taken by you: %s" %t)
    print("Average time taken by users who got this right: %s" %m_que_tavg[que][0])
    for x in q_graph[que]:
        if(l[x]==100):
            l[x]=-1
        else:
            l[x]=l[x]-1
    # update concept_score
        if x in con_score[q_level[que]]:
            con_score[q_level[que]][x] -= con_diff[x]
        else:
            con_score[q_level[que]][x] = con_diff[x]
    que_time[que]=t
    #c_average(m_que_tavg[que],t) 
    c_average(m_que_cavg[que],0)

def weak_concepts_fn():
    print("ANALYSIS")
    print("Weak Concepts")
    wl=[]
    table=PrettyTable(['Name','Avg Time','Avg Time(all users)','Avg Correctness','Question','Respective Correctness'])
    for x in xrange(len(l)):
        temp=[]
        temp.append(l[x])
        temp.append(x)
        wl.append(temp)
    wl.sort()
    for x in wl:
        if(x[0]<0):
            
            t=[]
            t.append(concepts[x[1]])
            t.append(int(np.mean(con_time[x[1]][0])))
            t.append(int(m_con_tavg[x[1]][0]))
            t.append(m_con_cavg[x[1]][0])
            t.append(con_que[x[1]])
            t.append(con_corr[x[1]])
            table.add_row(t)
            
    print(table)      
            
 
mval=-1
nq=-1
n=[-1]*len(q_graph.keys())
v=[0]*len(q_graph.keys())
        
#graph.keys() = question numbers
for x in xrange(len(q_graph.keys())):
    n[x]=q_graph.keys()[x]

print n
   
 #function to get the next question           
def next_que(level):
    mval=-1
    nq=-1
    n=[-1]*len(q_graph.keys())
    v=[0]*len(q_graph.keys())
            
    #graph.keys() = question numbers
    for x in xrange(len(q_graph.keys())):
        n[x]=q_graph.keys()[x]
                    
        #Check if the question is of required level
        if(q_level[x]==level and answered_q[n[x]]==0):
            for y in q_graph[n[x]]:
                if(l[y]==100):
                    v[x]=v[x]+1
                elif(l[y]<100 and l[y]>0):
                    v[x]=v[x]                    
                elif(l[y]<=0 and l[y]>-3):
                    v[x]=v[x]+3
                elif(l[y]<=-3):
                    v[x]=v[x]-10
        
            mval=max(v[x],mval)
            if(mval==v[x]):
                nq=n[x]
                
    answered_q[nq]=1
    return nq

def start_analysis():
    start=1
    print("Please answer the following Questions")
    l_checked[curr_level]=1
    for x in xrange(1000):
        total_que=total_que+1
        try:
            if (start ==1):
                start =0
                nq=random_q(curr_level)
                answered_q[nq]=1
            else:
                nq=next_que(curr_level)
          
            if(nq==-1):
                curr_level=curr_level+1
                if(curr_level > total_levels):
                    print("All levels cleared successfully!!!")
                    weak_concepts_fn()
                    break
                    print("Questions over in this level")
                continue
            
            cq=1
            t1=time.time()
            for x in range(len(question[nq])):
                print(question[nq][x])
                print("Answer is : %s" %ans[nq][x])
                response = raw_input()
                t2=time.time()
                if(is_correct(ans[nq][x],response)==0):
#                         correct_ans(nq)
                
                    wrong_ans(nq,int(t2-t1))
                    wrong=wrong+1
                    cq=0
                    break
            
            if(cq==1):
                correct_ans(nq,int(t2-t1))
            total_que=total_que+1

            
            if(wrong==2):
                curr_level=curr_level-1
                print("Level down : %s" %curr_level)
                
                if(l_checked[curr_level]==0):
                    l_checked[curr_level]=1
                else:
                    weak_concepts_fn()
                    break
                wrong=0
                total_que=0
            
            if(total_que!=0 and total_que%5==0):
                curr_level=curr_level+1
                print("Level up : %s" %curr_level)
                wrong=0
                if(l_checked[curr_level]==0):
                    l_checked[curr_level]=1
                else:
                    break
                
            if(curr_level >= total_levels):
                print("All levels cleared successfully!!!")
                weak_concepts_fn()
                break
            
            if(curr_level<0):
                print ("Level 0 concepts : Failed !!! ")
                weak_concepts_fn()
                break


        except (KeyboardInterrupt, EOFError, SystemExit):
            break












