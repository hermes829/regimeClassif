# helpful packages
import nltk
import os
import csv
import string
from gensim import corpora, models, similarities
from operator import itemgetter

# Set wd
os.chdir('/Users/janus829/Dropbox/Research/WardProjects/ThailandStories/')

# Loading in data from thaiclean.csv
dates=[]
sources=[]
stories=[]
with open('thaiclean.csv', 'rb') as d:
	reader=csv.reader(d)
	for row in reader:
		dates.append(row[1])
		sources.append(row[3])
		stories.append(row[4])

stories=stories[0:10]

# Remove punctuation
puncts = list(set(string.punctuation))
storiesNoPunct = [''.join([letter for letter in story if letter not in puncts]) for story in stories]

# Tokenize
storiesToken = [[word for word in story.lower().split()] for story in storiesNoPunct]

# Remove stop words
stoplist=nltk.corpus.stopwords.words('english')
storiesNoStop = [[word for word in story if word not in stoplist] for story in storiesToken]

# Lemmatize
wnl = nltk.stem.WordNetLemmatizer()
storiesLemm = [[wnl.lemmatize(word) for word in story] for story in storiesNoStop]

# Remove words that only occur once
allTokens = sum(storiesLemm, [])
singleTokens = set(word for word in set(allTokens) if allTokens.count(word) == 1)
storiesFin = [[word for word in story if word not in singleTokens] for story in storiesLemm]

# Prepping for LDA
dictionary = corpora.Dictionary(storiesFin)
corpus = [dictionary.doc2bow(story) for story in storiesFin]

tfidf = models.TfidfModel(corpus) 
corpus_tfidf = tfidf[corpus]

n_topics = 12

lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=n_topics)

for i in range(0, n_topics):
 temp = lda.show_topic(i, 10)
 terms = []
 for term in temp:
  terms.append(term[1])
 print "Top 10 terms for topic #" + str(i) + ": "+ ", ".join(terms)
 
print 
print 'Which LDA topic maximally describes a document?\n'
print 'Original document: ' + stories[1]
print 'Preprocessed document: ' + str(storiesFin[1])
print 'Matrix Market format: ' + str(corpus[1])
print 'Topic probability mixture: ' + str(lda[corpus[1]])
print 'Maximally probable topic: topic #' + str(max(lda[corpus[1]],key=itemgetter(1))[0])

import os
import csv

os.chdir('/Users/janus829/Dropbox/Research/WardProjects')

nyt = open('nyt_title_data.csv', 'rU') # check the structure of this file!
nyt_data = []
nyt_labels = []
csv_reader = csv.reader(nyt)

for line in csv_reader:
 nyt_labels.append(int(line[0]))
 nyt_data.append(line[1])

nyt.close()


from gensim import corpora, models, similarities
from itertools import chain
import nltk
from nltk.corpus import stopwords
from operator import itemgetter
import re

url_pattern = r'https?:\/\/(.*[\r\n]*)+'

documents = [nltk.clean_html(document) for document in nyt_data]
stoplist = stopwords.words('english')
texts = [[word for word in document.lower().split() if word not in stoplist]
 for document in documents]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

tfidf = models.TfidfModel(corpus) 
corpus_tfidf = tfidf[corpus]

#lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=100)
#lsi.print_topics(20)

n_topics = 60
lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=n_topics)

for i in range(0, n_topics):
 temp = lda.show_topic(i, 10)
 terms = []
 for term in temp:
  terms.append(term[1])
 print "Top 10 terms for topic #" + str(i) + ": "+ ", ".join(terms)
 
print 
print 'Which LDA topic maximally describes a document?\n'
print 'Original document: ' + documents[1]
print 'Preprocessed document: ' + str(texts[1])
print 'Matrix Market format: ' + str(corpus[1])
print 'Topic probability mixture: ' + str(lda[corpus[1]])
print 'Maximally probable topic: topic #' + str(max(lda[corpus[1]],key=itemgetter(1))[0])