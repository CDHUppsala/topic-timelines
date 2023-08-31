import os
import json
from sklearn.feature_extraction import text
from nltk.corpus import stopwords

# An import that should function both locally and when running an a remote server
try:
    from environment_configuration import *
except:
    from topics2themes.environment_configuration import *

if RUN_LOCALLY:
    from topic_model_constants import *
    from word2vec_term_similarity import *

else:
    from topics2themes.topic_model_constants import *
    from topics2themes.word2vec_term_similarity import *
    

"""
Nr of topics to retrieve
"""
NUMBER_OF_TOPICS = 50

"""
The topic modelling algorithm is rerun with a decrease number of requested topics
until the number of found stable topics are similar to the ones requested
The amont of similarity is set here.
"""

PROPORTION_OF_LESS_TOPIC_TO_ALLOW = 0.9

"""
Nr of words to display for each topic
"""
NR_OF_TOP_WORDS = 60

"""
Nr of most typical document to retrieve for each topic
"""

NR_OF_TOP_DOCUMENTS = 100

"""
Number of runs to check the stability of the retrieved topics.
Only topics that occur in all NUMBER_OF_RUNS runs will be
considered valid
"""
NUMBER_OF_RUNS = 50


"""
Mininimum overlap of retrieved terms to considered the retrieved topic as
the same topic of a another one
"""
OVERLAP_CUT_OFF = 0.6

"""
When counting overlap, outliers are removed. This sets percentage for what is to be retained
"""
PERCENTATE_NONE_OUTLIERS = 0.20


"""
Whether to use pre-processing (collocation detection and synonym clustering)
"""
PRE_PROCESS = False


"""
Mininimum occurrence in the corpus for a term to be included in the topic modelling
"""
MIN_DOCUMENT_FREQUENCY = 10

"""
Maximum occurrence in the corpus for a term to be included in the topic modelling
"""
MAX_DOCUMENT_FREQUENCY = 0.95

"""
If the same word occurs several times in a document, should that be counted just once (binary)
or should it be counted several times
"""
BINARY_TF = False

"""
Set sublinear_tf = True, which use log(tf), to lower the advantage for long documents
"""
SUBLINEAR_TF = False

"""
Mininimum occurrence in the corpus for a term to be included in the clustering.
"""
MIN_DOCUMENT_FREQUENCY_TO_INCLUDE_IN_CLUSTERING = 3

"""
The stop word file of user-defined stopiwords to use (Scikit learn stop words are also used)
"""
STOP_WORD_FILE = "stopwords.txt"

"""
The directories in which data is to be found. The data is to be in files with the ".txt" extension
in these directories. For each directory, there should also be a stance-label and a color associated with
the data
"""


DATA_LABEL_LIST = [{DATA_LABEL : "unmarked", DIRECTORY_NAME : "climate-news", LABEL_COLOR : GREEN },\
                   {DATA_LABEL : "marked", DIRECTORY_NAME : "empty", LABEL_COLOR : RED}]

TOPIC_MODEL_ALGORITHM = NMF_NAME


MIN_FREQUENCY_IN_COLLECTION_TO_INCLUDE_AS_TERM = 2

MAX_NR_OF_FEATURES = 10000

USE_IDF = True

NR_OF_ITERATIONS = 500

STOP_WORD_SET = set(stopwords.words('swedish'))

SHOW_ARGUMENTATION = False
SHOW_SENTIMENT = False

REMOVE_DUPLICATES = True

MIN_NGRAM_LENGTH_FOR_DUPLICATE = 50


def corpus_specific_text_cleaning(text):
    return text

CLEANING_METHOD = corpus_specific_text_cleaning

MANUAL_COLLOCATIONS = "manual_collocations.txt"

NUMBER_OF_SENTENCES_IN_SUMMARY = 3

def get_labels(doc_path):
    base_name = os.path.basename(doc_path)
    date_str = base_name[:10]
    labels = []
    labels.append(date_str)
    return labels
    
NR_OF_ITERATIONS = 500

ADDITIONAL_LABELS_METHOD = get_labels

STORE_IN_DATABASE = False
