import plot_timeline_from_files
import os

# A function that transforms from the filename to a html link to where the user is directed when clicking on the graph
def link_mapping(name):
    name = os.path.basename(name)
    url = name.split("_%URL%_")[1].replace("https__", "https://").replace("_", "/").replace(".txt", "")

    return url

    
def do_plot():
    outputdir = "diabetes"
    label_length = 60
    
    print("Start plotting")
    
    file_name_pdf = "diabetes"
    label_file = "diabetes_topics/diabetes_cluster_labels.txt"
    texts_topics_file = "diabetes_topics/diabetes_clustered.txt"
    
   
    timestamp_topics_dict = plot_timeline_from_files.make_plot_from_files(label_file, texts_topics_file, outputdir,  file_name_pdf, label_length=label_length, hours_between_label_dates=1, width_vertical_line=0.2, bar_transparency=0.3, bar_width=0.1, fontsize=7, use_separate_max_confidence_for_each_topic=True, circle_scale_factor=200, link_mapping_func=link_mapping)
    
do_plot()


