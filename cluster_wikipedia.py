import cluster_transformers
import os
import os.path
from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from datetime import datetime, date, timedelta
from sklearn.cluster import KMeans

    
def get_label(doc_path):
    base_name = os.path.basename(doc_path)
    date, nr = base_name.split("_")
    return date
  

to_remove = stopwords.words('english') + ["points", "per", "others", "three",  "two", "others", "near", "five", "least", "story", "first", "al", "declares", "reports", "held", "says", "across", "announces", "new", "approves", "allegedly", "people", "former", "suspends", "country", "leave", "including", "six", "four", "el", "cases", "ago", "one", "person", "increase", "due", "command", "alleged", "four", "seven", "eight", "nine", "ten", "eleven", "twelve", "another", "years", "old", "twenty", "prime"]



# Test-run
if __name__ == '__main__':

    numbers = [str(el) for el in range(0, 5000)]
    more_numbers = ["0"+el for el in numbers]
    number_stopwords = ["000"] + numbers + more_numbers + to_remove
    
    corpus = "wikipedia/2026_links"
   
    cluster_transformers.encode_sentences(corpus, output_dir="wikipedia_2026", n_clusters=45, transform_filename_method=get_label, stopwords = number_stopwords, nr_of_words_to_show=11, min_occ_in_corpus_for_keyword=25, min_nr_of_text_in_cluster=50,  fixed_global_min_cos=1.15, high_level_cluster_threshold=0.62, max_nr_of_text_in_cluster=200)
    

    
   

