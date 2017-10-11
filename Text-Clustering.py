'''
    Author: Siri Chandana Sambatur
    Email: sambatur.siri@gmail.com
    Date: 11th October 2017
'''

import csv
import re
from nltk.tokenize import word_tokenize
import operator
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.feature_selection import SelectKBest

uniqueWords = set()
countWords = {}
topWords=[]
def create_file():
    '''
        Extract the reviews from the file to analyze them
    '''
    with open('finefoods.csv','w') as op_file:
        spamwriter = csv.writer(op_file)
        count=0
        with open('finefoods.txt', 'r',encoding = "ISO-8859-1") as in_file:
            for line in in_file:
                if 'review/text' in line:
                    count+=1
                    line=line.strip('\n')
                    spamwriter.writerow([line.split(':')[1]])

def alpha_filter(w):
  # pattern to match word of non-alphabetical characters
  pattern = re.compile('[^a-zA-Z]')
  if (pattern.search(w)):
    return True
  else:
    return False

def tokenize_reviews():
    '''
        Preprocessing of the reviews to remove from the stopwords and the non alphabetical words.
    '''
    moreStopwords = open("LongStopWords.txt")
    words = moreStopwords.read()
    with open('finefoods.csv','r') as file:
        for line in file:
            tokens=word_tokenize(line)
            alphatokens = [w for w in tokens if  not alpha_filter(w)]
            words2lowercase = [w.lower() for w in alphatokens]
            morestoppedwords = [w for w in words2lowercase if not w in words]
            print(len(morestoppedwords))
            for w in morestoppedwords:
                uniqueWords.add(w)

    with open('uniquewords.txt','w') as file:
        countw=0
        for word in uniqueWords:
            countw+=1
            file.write(word)
            file.write(',')
        print("count is "+str(countw))

def top_words():
    '''
        Finding the top 500 words from all the reviews after the preprocessing of the reviews.
    '''
    with open('finefoods.csv','r') as file:
        for line in file:
            tokens=word_tokenize(line)
            print("1")
            for w in tokens:
                if w in uniqueWords:
                    print(w)
                    if w in countWords:
                        countWords[w]+=1;
                    else:
                        countWords[w]=1;
    sorted_counts = sorted(countWords.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_counts)
    with open('top500words.csv','w') as file:
        writer = csv.writer(file)
        count = 0
        for i in range(len(sorted_counts)):
            if(count<500):
                print(count)
                topWords.append(sorted_counts[i][0])
                writer.writerow([sorted_counts[i][0],sorted_counts[i][1]])
                count+=1

def vectorize_reviews():
    '''
        Vectorizing each review by the count of occurences of the top 500 words
    '''
    with open('VectorizedReviews.csv','w') as csvfile:
        csvfile.write('review')
        csvfile.write(',')
        for i in range(len(topWords)-1):
            csvfile.write(topWords[i])
            csvfile.write(',')
        csvfile.write(topWords[len(topWords)-1])
        csvfile.write('\n')

        with open('reviewIDs.txt','w') as txtfile:
            with open('finefoods.csv','r') as file:
                count=0
                for line in file:
                    txtfile.write(str(count)+"   ")
                    txtfile.write(line)
                    csvfile.write(str(count))
                    csvfile.write(',')
                    count+=1
                    tokens=word_tokenize(line)
                    for w in topWords:
                        wordCount=0
                        for word in tokens:
                            if w==word:
                                wordCount+=1
                        csvfile.write(str(wordCount))
                        csvfile.write(',')
                    csvfile.write('\n')

def read_topWords():
    with open("top500words.csv","r") as file:
        for line in file:
            line=line.strip()
            line=line.split(',')
            topWords.append(line[0])


def clustering():
    '''
        Clustering the reviews into ten different clusters and finding the top five features/words from
        each cluster and stored in the 'top5wordspercluster.txt' file.
    '''
    vecReviewsdf = pd.read_csv("VectorizedReviews.csv")
    del vecReviewsdf["review"]
    columns=list(vecReviewsdf.columns)
    print(columns)
    vecReviews = vecReviewsdf.values
    print(len(vecReviews[0]))
    print("before")
    kmeans = KMeans(n_clusters=10).fit(vecReviews)
    labels = kmeans.labels_
    centers= kmeans.cluster_centers_
    print(centers)
    with open("ClusterCenters.txt", "w") as file1:
        file1.write(str(centers))
    print("after labels")
    print(labels)
    clusters = [[] for i in range(10)]
    for i in range(len(labels)):
        print(1)
        clusters[labels[i]].append(vecReviews[i])
    with open("top5wordspercluster.txt","w") as file1:
        for i in range(len(clusters)):
            print("for cluster "+str(i))
            file1.write("for cluster "+str(i))
            clusterdf=pd.DataFrame(clusters[i])
            clusterdf.columns=columns
            sum={}
            for i in columns:
                sum[i]=clusterdf[i].sum()
            sorted_x = sorted(sum.items(), key=operator.itemgetter(1), reverse=True)
            print(str(sorted_x))
            for i in range(5):
                print(sorted_x[i])
                file1.write(str(sorted_x[i]))
            file1.write('\n')



create_file()
tokenize_reviews()
top_words()
vectorize_reviews()
#read_topWords()
clustering()
