How to use with Topics2Themes
================================


Topics2Themes needs to be configured to use the
the ADDITIONAL_LABELS_METHOD, and to let that one
return exact ONE label, which is the date with which a document is associated
For instance, as follows:


```
    ADDITIONAL_LABELS_METHOD = get_labels
    def get_labels(doc_path):
        base_name = os.path.basename(doc_path)
        date_str = base_name[:10]
        labels = []
        labels.append(date_str)
        return labels
'''

See example in ![topic_model_configuration.py](topic_model_configuration.py)
