# Summarizing Reviews using Text Clustering

The reviews from [Amazon Fine Foods Reviews](http://snap.stanford.edu/data/web-FineFoods.html) have been extracted and analyzed using vectorization technique. All these reviews have been clustered based on the words used in the reviews and then each of the clusters is analyzed to find correlation between the words and hence correlation between the reviews.
The number of reviews present in this dataset are 568454 and these reviews are clustered in 10 different clusters using K-means algorithm

The files generated/used for this analyziz are-
1) Text-Clustering.py- contains the code to perform all the necessary analysis
2) finefoods.txt- is the dataset that is to be downloaded and placed in this folder
3) reviewIDs.txt - is a file that will be generated to map each review to an unique ID
4) VectorizedReviews.csv- It will vectorize all the reviews based on the occurences of the top 500 words in each review. The size of this matrix is number of reviews * 500.

## Data Preprocessing 
The following are the preprocessing steps that are done-

1) Extract all the reviews from the dataset and tokenize each review
2) Extracted English words
3) Removed all the words from the 'LongStopWords.txt'
4) Find the unique words that are used in all the reviews
5) Vectorized the reviews


## Running the Project
Open terminal on MacOS or command prompt on words and run the .py file as follows-

	python Text-Clustering.py

## Conclusion
After all the analysis, the following is the results that have been obtained-

1) the top 500 words that have occured frequently in all the reviews in the dataset
2) 10 clusters of reviews
3) top 5 words from each cluster and there frequency within the cluster
