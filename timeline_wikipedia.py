import plot_timeline_from_files
import os
import json
import csv

linkmappings = {}
with open("wikipedia/linkmappings.csv") as lm:
    r = csv.reader(lm, delimiter='\t', quotechar='|')
    for row in r:
      linkmappings[row[0]] = row[1]
      
popupmappings = {}
with open("wikipedia/popupmappings.csv") as pm:
    r_pm = csv.reader(pm, delimiter='\t', quotechar='|')
    for row in r_pm:
      popupmappings[row[0]] = row[1].strip()
        

def link_mapping(name, dict=None):
    return linkmappings[name]

def popup_mapping(name, dict=None):
    return popupmappings[name]
    
def do_plot():
    outputdir = "time_line_wikipedia"
    label_length = 100
    use_date_format = True
    
    print("Start plotting")
    
    
    # Agglomerative standard
    label_file = "wikipedia_2026/2026_links_cluster_labels.txt"
    texts_topics_file = "wikipedia_2026/2026_links_clustered.txt"
    order_mapping_file = "wikipedia_2026/2026_links_high_level_clusters.txt"
    file_name = "wikipedia_2026"
    file_name_pdf = "wikipedia_2026_pdf"
    color_file = "wikipedia_2026/2026_links_colour_values_high_level_clusters.txt"


    # Plot a pdf
    timestamp_topics_dict = plot_timeline_from_files.make_plot_from_files(label_file, texts_topics_file, outputdir,  file_name_pdf, label_length=label_length, hours_between_label_dates=0.52, width_vertical_line=0.0001, transparency_vertical_line=0.05, fontsize=7,  use_separate_max_confidence_for_each_topic=True, marker_scale_factor=80, marker_transparency=0.4, use_orig_nr=False, tip_size=1, order_mapping_file = order_mapping_file, color_file=color_file, show_months_labels=True, extra_x_length=1)
    
    # Plot an interactive html file
    timestamp_topics_dict = plot_timeline_from_files.make_plot_from_files(label_file, texts_topics_file, outputdir, file_name, label_length=label_length, hours_between_label_dates=0.52, width_vertical_line=0.01, transparency_vertical_line=0.1, fontsize=7,  use_separate_max_confidence_for_each_topic=True, marker_scale_factor=80, marker_transparency=0.6, use_orig_nr=False, tip_size=5,order_mapping_file = order_mapping_file, color_file=color_file, link_mapping_func=link_mapping, popup_mapping_func=popup_mapping, show_months_labels=True, extra_x_length=1)
        
    
do_plot()
