

import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib.markers as markers
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator, MaxNLocator, FixedLocator)
from matplotlib import cm
import math
import matplotlib.colors as colors
import os
import matplotlib.dates as mdates
from math import modf
import sys
import datetime
import matplotlib
from collections import Counter
import re


plt.rcParams["font.family"] = "monospace"
     
############################
# 1. Reading data from files
############################

def get_labels(label_file):
    labels = []
    with open(label_file) as lb:
        for line in lb:
            labels.append(line.strip().split("\t"))
    return labels


def get_document_info(texts_topics_file_name, popup_link):
    # Get timestamps
    base_name_timestamp_mapping_dict = {}
    with open(texts_topics_file_name) as text_topics_file:
        for line in text_topics_file:
            sp = line.strip().split("\t")
            str_date = sp[1]
            
            timestamp = np.datetime64(str_date)
            
            base_name = os.path.basename(sp[0])
            base_name_timestamp_mapping_dict[base_name] = timestamp
            
    # Loop through the documents, and collect topics for the documents. # Store in document_info, with "base_name" of the document as the key
    document_info = {}
    max_topic_confidence_for_topic = {}
    with open(texts_topics_file_name) as text_topics_file:
    
        for line in text_topics_file:
            sp = line.strip().split("\t")
            base_name = os.path.basename(sp[0])
            document_topics = []
            nr_of_topics = None
            for topic_nr, column_content in enumerate(sp[2:]):
                if column_content == "":
                    break
                column_content = float(column_content)
                if column_content > 0: # Topic included in this document
                    terms = ""
                    if popup_link:
                        if "" in sp:
                            index_for_terms = sp.index("") + topic_nr + 1
                            if len(sp) > index_for_terms:
                                terms = sp[index_for_terms]
                        else:
                            print("column_content", column_content)
                            print("Error. Row is missing keywords: ", sp)
                            exit()
                
                    topic_info = {}
                    topic_info["terms_found_in_text"] = terms
                    topic_info["topic_index"] = topic_nr
                    topic_info["topic_confidence"] = column_content
                    document_topics.append(topic_info)
                    
                    # Record information on max confidence for topic in max_topic_confidence_for_topic
                    if topic_info["topic_index"] not in max_topic_confidence_for_topic or \
                        topic_info["topic_confidence"] > max_topic_confidence_for_topic[topic_info["topic_index"]]:
                        max_topic_confidence_for_topic[topic_info["topic_index"]] = topic_info["topic_confidence"]
                    
                if len(document_topics) > 1:
                    "More than one topic"
                    
            assert(base_name not in document_info)
            document_info[base_name] = document_topics
  
    return document_info, max_topic_confidence_for_topic, base_name_timestamp_mapping_dict
        

# Collect "meta_data_dict"
# In "meta_data_dict": Each item contains a date and the list of documents (basename for document) associated
# with this date. E.g.
# 1964-01-01 ['file_1.txt', 'file_2.txt', 'file_3.txt']
def get_meta_data_from_dict(base_name_timestamp_mapping_dict):
    meta_data_dict = {}

    min_timestamp = np.datetime64('9999-01-02')
    max_timestamp = np.datetime64('0000-01-02')
    
    max_decimal_part_for_year = {}
    
    for base_name, timestamp in base_name_timestamp_mapping_dict.items():
        if timestamp not in meta_data_dict:
            meta_data_dict[timestamp] = []
        meta_data_dict[timestamp].append(base_name)

    print("Nr of dates found in metadata", len(meta_data_dict.keys()))
    return meta_data_dict, min_timestamp, max_timestamp
  
  
  
#########
# 2. Functions related to the user ordering of the topics
########

def get_y_value_for_user_topic_nr(original_nr, order_mapping_flattened, order_mapping):
    if not order_mapping:
        return original_nr
    else: # User don't use 0
        original_nr = original_nr + 1
        ret = order_mapping_flattened.index(original_nr)
        return ret
 
 
def get_order_mapping_flattend(order_list):
    if not order_list: #None
        return order_list
    flat_list = []
    for item in order_list:
        if type(item) is list:
            flat_list.extend(item)
        else:
            flat_list.append(item)
            
    counter = Counter(flat_list)
    potentinal_dupblicates = ([dbl for dbl in counter if counter[dbl] > 1])
    if len(potentinal_dupblicates) > 0:
        print("There are dublicates in 'order_mapping', remove them. The following: ", potentinal_dupblicates)
        exit()
        
    return flat_list
   
#####################################
# 3. Getting the names of the topics
#####################################

def get_topic_names(labels, translation_dict, file_name, outputdir, label_length, order_mapping_flattened):
    # Give the topics the labels to show to the user and the number for the topic to show to the user
    topic_names = []
    long_topic_names = []

    for nr, terms_list in enumerate(labels):
        repr_terms = []
        for t in terms_list:
 
            # TODO: Update code here
            term_to_pick_as_rep = "123456789123456789123456789123456789123456789123456789"
    
            for s in t.split("/"):
                if len(s.strip()) < len(term_to_pick_as_rep):
                    term_to_pick_as_rep = s.strip()
            repr_terms.append(term_to_pick_as_rep.strip())
            
        if translation_dict:
            repr_terms_new = repr_terms[:10] #TODO: Don't hard-code the length
            repr_terms = []
            for r in repr_terms_new:
                r_strip = r.strip()
                if r_strip in translation_dict:
                    term_to_add = translation_dict[r_strip]
                else:
                    term_to_add = r_strip
                    print(r_strip)
                repr_terms.append(term_to_add)
        third_length = int(len(repr_terms)/3)

        topic_name_long = ", ".join(repr_terms)
        long_topic_names.append(str(nr+1) + " " + topic_name_long)
            
        topic_name = topic_name_long[0:label_length]
        
        
        if topic_name[-1] == " ":
            topic_name = topic_name[:-1] + "."
        if topic_name[-2] == "," or topic_name[-2] == " ":
            topic_name = topic_name[:-2] + ".."
        topic_name = topic_name + "..."
        nr_str = str(nr + 1)
        if order_mapping_flattened:
            try:
                mapped_nr = str(order_mapping_flattened[nr])
            except IndexError:
                print(nr, "not an index in", order_mapping_flattened)
                print((list(range(1, len(order_mapping_flattened) + 1))))
                print(sorted(order_mapping_flattened))
                raise(IndexError)
        else:
            mapped_nr = ""
        if len(nr_str) == 1:
            nr_str = " " + nr_str
        topic_names.append(nr_str + ": " + topic_name)
    

    if not os.path.exists(outputdir):
        os.mkdir(outputdir)
    write_long_topic_names = os.path.join(outputdir, file_name + "_long_topic_names.txt")
    with open(write_long_topic_names, "w") as wltn:
        for el in long_topic_names:
            wltn.write(el + "\n\n")

    return topic_names
    
#########################################################
# 4. Get how much the vertical lines are to be spread out
#########################################################

def get_spread_between_vertical_lines(hours_between_label_dates):
    if hours_between_label_dates == 0:
        print("'hours_between_label_dates' needs to be larger than 0")
        exit()
    
    if hours_between_label_dates >= 1:
        part = abs(hours_between_label_dates)
        if part == 0:
            print("Warning the spread seems to be 0.")
            exit()
        spread_distance = np.timedelta64(part, 'h')
        print("Texts with the same timestamp will be spread out with ", spread_distance, "hours")
    else:
        seconds = math.ceil(3600*hours_between_label_dates)
        spread_distance = np.timedelta64(seconds, 's')
        print("Texts with the same timestamp will be spread out with ", spread_distance, "seconds")
        
    return spread_distance
    
#########################################################################
# 5. Create a dictionary with spread out timestamps and associated topics
#########################################################################

def get_timestamp_topic_dict(meta_data_dict, document_info, user_defined_min_timestamp, user_defined_max_timestamp, spread_distance):
    # Create timestamp_topics_dict
    # Where the each element is a key with a timestamp, and
    # which in turn contains a dictionary of confidence for the
    # differen topics for this timestamp
    # 1990-12-28T03 {16: 0.06963693325855479, 44: 0.08608091116481784, 47: 0.28642090183730934, 57: 0.4293435359283798}
    timestamps = sorted(meta_data_dict.keys())
    timestamp_topics_dict = {}
    timestamp_basename_dict = {} # To be able to connect timestamps to filename
    max_topic_confidence = 0
    link_found_terms_mapping = {}
    
    # Experimental, to show tool tip
    timestamp_terms_found_dict = {}
    
    latest_timestamp_used_so_far = np.datetime64('0000-01-02')

    if user_defined_min_timestamp:
        min_timestamp_user_defined = np.datetime64(user_defined_min_timestamp)
    if user_defined_max_timestamp:
        max_timestamp_user_defined = np.datetime64(user_defined_max_timestamp)

    total_nr_of_topics_found_in_documents = 0
    base_names_without_associated_topics = []
    for i in range(0, len(timestamps)):
        timestamp = timestamps[i]
 
        # Outside of user-define range
        if user_defined_max_timestamp and np.datetime64(timestamp) > max_timestamp_user_defined:
            continue
        if user_defined_min_timestamp and np.datetime64(timestamp) < min_timestamp_user_defined:
            continue

        # The previously spread out time stamps have been spread out so much so that
        # they reach the next "real" timestamp
        if timestamp <= latest_timestamp_used_so_far:
            print("The timestamps are spread out so much so that they collide with coming texts. Decrease the 'hours_between_label_dates' value when calling the visualisation")
            print("timestamp", timestamp)
            print("latest_timestamp_used_so_far", latest_timestamp_used_so_far)
            exit()
        
        # All texts with this timestamp
        base_names = sorted(meta_data_dict[timestamp]) #Collected unsorted, so need to sort here
        
        # Experimental to show tool tip
        timestamp_terms_found_dict[timestamp] = {}
        
        # Add one element in timestamp_topics_dict for each basename with topic
        for base_name in base_names:
            year = timestamp.astype(object).year
            
            if base_name in document_info:
                assert(timestamp not in timestamp_topics_dict)
                timestamp_topics_dict[timestamp] = {}
                            
                for document_topic in document_info[base_name]:
                        
                    total_nr_of_topics_found_in_documents = total_nr_of_topics_found_in_documents + 1
                    topic_index = document_topic["topic_index"]
                    topic_confidence = document_topic["topic_confidence"]
                    
                    timestamp_topics_dict[timestamp][topic_index] = topic_confidence
                    
                    # Experimental code, to show tooltip
                    timestamp_terms_found_dict[timestamp][topic_index] = document_topic["terms_found_in_text"]
                    
                    # Gather max values
                    if topic_confidence > max_topic_confidence:
                        max_topic_confidence = topic_confidence
                    
            else:
                base_names_without_associated_topics.append(base_name)
                        
            #To be able to connect timestamps to filename, for links
            assert(timestamp not in timestamp_basename_dict)
            timestamp_basename_dict[timestamp] = base_name
            
            #Create a new timpestamp to spread out texts that would otherwise get the same x-value
            old_timestamp = timestamp
            timestamp = timestamp + spread_distance
            assert(timestamp != old_timestamp)

            latest_timestamp_used_so_far = timestamp
            
            # Experimental for tool tip
            timestamp_terms_found_dict[timestamp] = {}
            
            
    print("nr of documents without associated topics: ", len(base_names_without_associated_topics))
    print("total_nr_of_topics_found_in_documents", total_nr_of_topics_found_in_documents)
    
    return timestamp_topics_dict, timestamp_terms_found_dict, link_found_terms_mapping, timestamp_basename_dict


#######################################
# 6. Get min and max timestamps
#######################################
def get_min_max_timestamp(meta_data_dict, user_defined_min_timestamp, user_defined_max_timestamp, extra_x_length):

    sorted_dates = sorted(meta_data_dict.keys())
    min_timestamp = sorted_dates[0]
    max_timestamp = sorted_dates[-1]
        
    if user_defined_min_timestamp:
        min_timestamp = np.datetime64(user_defined_min_timestamp)
    if user_defined_max_timestamp:
        max_timestamp = np.datetime64(user_defined_max_timestamp)
        
    min_timestamp = min_timestamp - (max_timestamp - min_timestamp)*extra_x_length
    max_timestamp = max_timestamp + (max_timestamp - min_timestamp)*extra_x_length

    print("min_timestamp", min_timestamp)
    print("max_timestamp", max_timestamp)
    
    min_year = min_timestamp.astype(object).year + 1
    max_year = max_timestamp.astype(object).year + 1
    years_to_plot = range(min_year, max_year)
    

    return min_timestamp, max_timestamp, min_year, max_year, years_to_plot

####################################
# 7. Functions related to colour use
####################################

def update_color(current_color_number, index_for_color_number, order_mapping):
    if not order_mapping:
        return current_color_number + 1, index_for_color_number
    
    if not type(order_mapping[current_color_number]) is list:
        return current_color_number + 1, index_for_color_number
    
    if index_for_color_number + 1 >= len(order_mapping[current_color_number]):
         return current_color_number + 1, 0
    else:
        return current_color_number, index_for_color_number + 1

def get_weaker_form_of_named_color(color_name, transparancy):
     rgb = list(colors.to_rgb(color_name))
     rgb.append(transparancy)
     return rgb
     
def get_color_mapping(topic_names, order_mapping, order_colors):
    previous_color_number = 0
    current_color_number = 0 # index that is counted
    index_for_color_number = 0
    current_simplifyed_color = get_weaker_form_of_named_color("lavender", 0.4)
    current_stronger_color =  "mediumpurple"
    color_mapping = {} # Mapping from user-shown topic nr:s to colors
    color_mapping_stronger = {}
    ys_when_color_is_updated = [] # To be able to draw a line between the colors-shifts
    
    # Only used if order_colors is given
    current_index_in_order_colors = 0
    how_much_weaker = 0.02
    
    for el in range(0, len(topic_names)):
        if order_mapping:
            if type(order_mapping[current_color_number]) is list:
                user_topic_nr = order_mapping[current_color_number][index_for_color_number]
            else:
                user_topic_nr = order_mapping[current_color_number]
            
            current_color_number, index_for_color_number = update_color(current_color_number, index_for_color_number, order_mapping)
         
            if not order_colors: # no color given by the user
                color_mapping[user_topic_nr] = current_simplifyed_color
                color_mapping_stronger[user_topic_nr] = current_stronger_color
            else:
                color_mapping_stronger[user_topic_nr] = order_colors[current_index_in_order_colors]
                color_mapping[user_topic_nr] = get_weaker_form_of_named_color(order_colors[current_index_in_order_colors], 0.09 + how_much_weaker)
                how_much_weaker = how_much_weaker * -1
            if current_color_number != previous_color_number: #color is updated
                
                current_index_in_order_colors = current_index_in_order_colors + 1
                how_much_weaker = 0.02
                
                ys_when_color_is_updated.append(el)
                
                if current_simplifyed_color == get_weaker_form_of_named_color("lavender", 0.4):
                    current_simplifyed_color = get_weaker_form_of_named_color("honeydew", 0.5)
                    current_stronger_color = "darkseagreen"
                else:
                    current_simplifyed_color = get_weaker_form_of_named_color("lavender", 0.4)
                    current_stronger_color = "mediumpurple"

            previous_color_number = current_color_number
        else: # Use every other
            color_mapping[el + 1] = current_simplifyed_color
            if current_simplifyed_color == get_weaker_form_of_named_color("lavender", 0.4):
                current_simplifyed_color = get_weaker_form_of_named_color("honeydew", 0.5)
            else:
                current_simplifyed_color = get_weaker_form_of_named_color("lavender", 0.4)
                
    return color_mapping, color_mapping_stronger, ys_when_color_is_updated

#########################
# 8. Write to outputfile
##########################
def write_to_outputfile(plt, outputdir, file_name, link_mapping_func, popup_link, link_found_terms_mapping):
    
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)
    
    if link_mapping_func:
        save_to_svg = os.path.join(outputdir, file_name + ".html")
        plt.savefig(save_to_svg, dpi = 700, transparent=False, format="svg")
        print("Save plot in: ", save_to_svg)
        
        
        with open(os.path.join(outputdir, file_name + ".html")) as orig_file:
            content = orig_file.read()
            p = re.compile('<a xlink:href=".*">')
            matches = p.findall(content)
            for m in matches:
                
                link = m.replace("<a xlink:href=\"", "").replace("\">", "")
                                
                title_part = "Click to read text"
                if popup_link:
                    """ # TODO: Implement popup of important words
                    if link in link_found_terms_mapping:
                        
                        tool_tip_dict = {}
                        for key, value in link_found_terms_mapping[link].items():
                            # Another index is shown to the user, so use this index in the tool tip
                            # Also add by + 1, because start with 1 (not 0) to user
                            tool_tip_dict[key + 1] = value
                        
                        title_part = "<title>" + str(tool_tip_dict) + "</title>"
                    else:
                    """
                    title_part = "<title>" + link + "</title>"
                    
                popup_link = f'<a href="#" onclick="const myWindow = window.open(\'{link}\', \'yourWindowName\', \'width=200,height=150\');myWindow.blur();focus();myWindow.resizeTo(screen.width/5,screen.height);window.opener.focus()">{title_part}'
                content = content.replace(m, popup_link)
                
                
            with open(os.path.join(outputdir, file_name + "_popup.html"), "w") as write_to:
                write_to.write(content)
                
    else:
        save_to_pdf = os.path.join(outputdir, file_name + ".pdf")
        plt.savefig(save_to_pdf, dpi = 700, transparent=False, format="pdf")
        print("Save plot in: ", save_to_pdf)
 
#######
# Start
########

def make_plot_from_files(label_file, texts_topics_file, outputdir, file_name, label_length=20, normalise_for_nr_of_texts=False,  vertical_line_to_represent_nr_of_documents=False, hours_between_label_dates=1, width_vertical_line=0.0000001, extra_x_length=0.005, order_mapping=None, use_separate_max_confidence_for_each_topic=True, link_mapping_func=None, link_mapping_dict=None, bar_width=0.1, bar_transparency=0.2, circle_scale_factor=400, translation_dict = {}, user_defined_min_timestamp=None, user_defined_max_timestamp=None, order_colors=None, fontsize=9, popup_link=False, min_confidence_proportion_to_plot = 0.0, user_topic_numbers_to_include = []):

    if user_topic_numbers_to_include:
        file_name = file_name + "_topics_" + "_".join([str(i) for i in user_topic_numbers_to_include])
 
    if user_defined_min_timestamp:
        file_name = file_name + "_from_" + ''.join(c for c in user_defined_min_timestamp if c.isnumeric())
    if user_defined_max_timestamp:
        file_name = file_name + "_to_" + ''.join(c for c in user_defined_max_timestamp if c.isnumeric())

        
    # 1. Read data on timestamps, texts and topics from files
    ##########################################################
    labels = get_labels(label_file)
    document_info, max_topic_confidence_for_topic, base_name_timestamp_mapping_dict = get_document_info(texts_topics_file, popup_link)
    print(max_topic_confidence_for_topic)
    max_topic_confidence = max(max_topic_confidence_for_topic.values())
    print(max_topic_confidence)
    
    
    meta_data_dict, min_timestamp, max_timestamp = get_meta_data_from_dict(base_name_timestamp_mapping_dict)
    print("Nr of documents found", len(document_info.items()))
    
    # 2. Get and check user ordering of the topics
    ###############################################
    order_mapping_flattened = get_order_mapping_flattend(order_mapping)
    
    # 3. Give the topics the labels to show to the user and the number for the topic to show to the user
    #####################################################################################################
    topic_names = get_topic_names(labels, translation_dict, file_name, outputdir, label_length, order_mapping_flattened)
    
    # 4. How much to spread the vertical lines
    ##########################################
    spread_distance = get_spread_between_vertical_lines(hours_between_label_dates)
    
    # 5. Create a dictionary with timestamps spread out and topics
    ##############################################################
    timestamp_topics_dict, timestamp_terms_found_dict, link_found_terms_mapping, timestamp_basename_dict = get_timestamp_topic_dict(meta_data_dict, document_info, user_defined_min_timestamp, user_defined_max_timestamp, spread_distance)

    # 6. Determine min and max timestamps
    ######################################
    min_timestamp, max_timestamp, min_year, max_year, years_to_plot = get_min_max_timestamp(meta_data_dict, user_defined_min_timestamp, user_defined_max_timestamp, extra_x_length)
    
    # 7. Make a colour mapping
    ############################
    color_mapping, color_mapping_stronger, ys_when_color_is_updated  = get_color_mapping(topic_names, order_mapping, order_colors)
        
    # Construt the canvas to plot on
    #################################
    fig, ax1 = plt.subplots(figsize = (11.693, 8.268))
    ax1.set(ylim=(-len(topic_names) - 0.5, 0.5))
    #ax1.set(xlim=(min_timestamp-20, max_timestamp+20))

    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_minor_locator(mdates.MonthLocator())
    
    
    # Create the background, i.e., make the horizontal colors and lines
    ####################################################################
    
    topic_names_resorted = [0]*len(topic_names) # For the y-tick-labels
    topic_names_resorted_only_numbers = [0]*len(topic_names) # For left side y-tick-labels
    y_width = 0.5
    for user_topic_nr in range(0, len(topic_names), 1):
        
        y = get_y_value_for_user_topic_nr(user_topic_nr, order_mapping_flattened, order_mapping)
        
        print(topic_names_resorted[y])
        print(topic_names[user_topic_nr])
        topic_names_resorted[y] = topic_names[user_topic_nr]
        topic_names_resorted_only_numbers[y] = str(user_topic_nr + 1)
        ty = -y
        
        # The horizontal line in the middle of each topic
        plt.axhline(y=ty, linewidth=0.1, color='black', zorder = -50)
        
        current_color = color_mapping[user_topic_nr + 1]
        
        if order_mapping:
            edgecolor = color_mapping_stronger[user_topic_nr + 1]
        
        # The colored filling
        if order_mapping:
            ax1.fill([min_timestamp, max_timestamp, max_timestamp, min_timestamp, min_timestamp], [ty - y_width, ty - y_width, ty + y_width, ty + y_width, ty - y_width], color = current_color, edgecolor = edgecolor, linewidth=0.2, linestyle="solid", zorder = -10000)
        else:
            ax1.fill([min_timestamp, max_timestamp, max_timestamp, min_timestamp, min_timestamp], [ty - y_width, ty - y_width, ty + y_width, ty + y_width, ty - y_width], color = current_color, linewidth=0.1, linestyle="solid", zorder = -10000)
            if current_color == get_weaker_form_of_named_color("lavender", 0.4):
            #TODO: a better solution for comparing to get_weaker_form_of_named_color
                dots_color = "mediumpurple"
            else:
                dots_color = "darkseagreen"
                    
            for year_to_plot in years_to_plot:
                first_day = np.datetime64(str(year_to_plot) + "-01-01")
                middle_year = np.datetime64(str(year_to_plot) + "-07-01")
                ax1.scatter(first_day,-y-y_width, color=dots_color, zorder=-50, marker='D', s=0.1)
                ax1.scatter(middle_year,-y-y_width, color=dots_color, zorder=-50, marker='D', s=0.005)
    for year_to_plot in years_to_plot:
        first_day = np.datetime64(str(year_to_plot) + "-01-01")
        middle_year = np.datetime64(str(year_to_plot) + "-07-01")
        ax1.scatter(first_day, 0+y_width, color="mediumpurple", zorder=-50, marker='D', s=0.1)
        ax1.scatter(middle_year, 0+y_width, color="mediumpurple", zorder=-50, marker='D', s=0.01)
    
    print(topic_names_resorted)
    print(len(topic_names_resorted))
    # lines separating the colors
    if order_mapping:
        separating_color = "mediumpurple"
        plt.axhline(y=+y_width, linewidth=1, color="black", zorder = -40) #start with a black line
        if not order_colors:
            for y in ys_when_color_is_updated[:-1]:
                if separating_color == "mediumpurple":
                    separating_color = "darkseagreen"
                else:
                    separating_color = "mediumpurple"
                plt.axhline(y=-y-y_width, linewidth=1, color=separating_color, zorder = -40)
        plt.axhline(y=-ys_when_color_is_updated[-1]-y_width, linewidth=1, color="black", zorder = -40) # End with a black line
        plt.yticks([+y_width] + [-y-y_width for y in ys_when_color_is_updated], [], minor=False) # Mark color change with y-tick-lines also
        plt.yticks([-y for y in range(0, len(topic_names), 1)], topic_names_resorted)
    else:
        plt.yticks([-y for y in range(0, len(topic_names), 1)], topic_names_resorted, minor=False)
    
    #ax1.set_xticklabels(ax1.xaxis.get_majorticklabels(), rotation=270)
    plt.xticks(rotation=270)
    ax1.yaxis.set_label_position("right")
    ax1.yaxis.tick_right()
    
    # Add topic number in small letters to the left
    for y in range(0, len(topic_names)):
        if order_mapping_flattened:
            ax1.text(min_timestamp-15, -y, order_mapping_flattened[y], fontsize=fontsize-1)
        else:
            ax1.text(min_timestamp-15, -y, str(y+1), fontsize=fontsize-1)
        
 
    # Make colors markings in the beginning and end of the timeline
    # And extra horisonal, dotted lines when 'order_mapping' is given
    if order_mapping:
        striped_transpar = 1
        for y in range(0, len(topic_names)):
            user_nr = order_mapping_flattened[y]
            color_to_use = color_mapping_stronger[user_nr]
            
            if striped_transpar:
                color_to_use = get_weaker_form_of_named_color(color_to_use, 0.1)
            
            if y not in ys_when_color_is_updated:
                if striped_transpar:
                    for year_to_plot in years_to_plot:
                        first_day = np.datetime64(str(year_to_plot) + "-01-01")
                        middle_year = np.datetime64(str(year_to_plot) + "-07-01")
                        ax1.scatter(first_day,-y-0.5, color=color_mapping_stronger[user_nr], facecolor=color_mapping[user_nr], zorder=-50, marker='D', s=0.1)
                        ax1.scatter(middle_year,-y-0.5, color=color_mapping_stronger[user_nr], facecolor=color_mapping[user_nr], zorder=-50, marker='D', s=0.01)
                else:
                    ax1.axhline(-y-0.5, color=color_mapping_stronger[user_nr], zorder=-50, linewidth=0.1, linestyle="solid")
            if striped_transpar == 1:
                striped_transpar = 0
            else:
                striped_transpar = 1
            
    print("Created background")
    
    
    # Plot a vertical line for each document. And for each document, plot its corresponding topics
    ###############################################################################################
    nr_of_plotted = 0
    bar_height = 0.5
    
    for timestamp, topic_dict in timestamp_topics_dict.items():
        
        original_timestamp = timestamp
        year = timestamp.astype(object).year
       
        # The vertical line, representing documents
        plt.axvline(x=timestamp, linewidth=width_vertical_line, color= [0.95, 0.95, 0.95, 1], zorder = -1000)
        
        # Plot the occurrences of topics in the documents
        
        for topic_index, confidence in topic_dict.items():
            
            # If the user has specfied to only include some topics
            # and the current topic is not among them
            # don't plot anything
            # (+1, because starting to count at 1 in visualisation)
            if user_topic_numbers_to_include and topic_index+1 not in user_topic_numbers_to_include:
                continue
            
            y_value_for_topic_nr = get_y_value_for_user_topic_nr(topic_index, order_mapping_flattened, order_mapping)
               
            max_confidence_for_topic = max_topic_confidence_for_topic[topic_index]
            
            min_confidence_proportion_to_plot
            
            confidence_proportion = confidence/max_confidence_for_topic
            if confidence_proportion < min_confidence_proportion_to_plot:
                continue

            ty = -y_value_for_topic_nr
            if use_separate_max_confidence_for_each_topic:
                cw2 = bar_height*confidence/max_confidence_for_topic
            else:
                cw2 = bar_height*confidence/max_topic_confidence
            
            
            # The actual vertical bar showing the strength of the topic for the text
            ax1.plot([timestamp, timestamp], [ty + cw2, ty - cw2], '-', markersize=0, color = [0, 0, 0, bar_transparency], linewidth=bar_width, zorder = -2*cw2)
                        

            s1 = ax1.scatter([timestamp], [ty], color=[0, 0, 0, bar_transparency], facecolor=[0, 0, 0, bar_transparency/5], marker="o", s=cw2*cw2*circle_scale_factor, linewidth=0.1, zorder=-cw2*20)
            s2 = ax1.scatter([timestamp, timestamp], [ty + cw2,  ty - cw2], color=[0, 0, 0, bar_transparency], facecolor=[0, 0, 0, bar_transparency], marker="s", s=cw2*bar_width*1.5, linewidth=0.1, zorder=-cw2)

            if link_mapping_func:
                link = link_mapping_func(timestamp_basename_dict[timestamp])
                s1.set_urls([link, link]) # Seems to be a bug, you need at least two links, although it's only one scatter point
                s2.set_urls([link, link])
                # Can't set urls on lines, only scatter markers. So add three scatter markers with links
                
                link_found_terms_mapping[link] = timestamp_terms_found_dict[timestamp]
               
            nr_of_plotted = nr_of_plotted + 1
            if nr_of_plotted % 100 == 0:
                print(timestamp, end=" ", flush=True)
    
    
    plt.yticks(fontsize=fontsize)
    plt.xticks(fontsize=6)
    plt.tight_layout()

    # 8. Write to outputfile, and create links if that is configured
    ################################################################
    
    write_to_outputfile(plt, outputdir, file_name, link_mapping_func, popup_link, link_found_terms_mapping)
   
    return timestamp_topics_dict


