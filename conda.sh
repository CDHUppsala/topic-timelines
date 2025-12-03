conda create --name topic_timeline python=3.10
conda install anaconda::scikit-learn
conda install anaconda::nltk
conda install conda-forge::sentence-transformers
conda install pytorch::pytorch
conda install conda-forge::matplotlib
conda install anaconda::numpy=1.26.4

# Need to do:
# python
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt_tab')
# exit()
