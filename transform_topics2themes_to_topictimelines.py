import os
import os.path
import json
import numpy as np


def write_document_info(model_file, metadata_file_name, show_to_user_nr_topic_index_mapping, output_dir):

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        
    file_name = "texts_topics_" + os.path.basename(model_file).replace(".json", ".txt")
    

    obj = None
    with open(model_file, 'r') as f:
        data = f.read()
        obj = json.loads(data)
    
    # Get timestamps
    base_name_timestamp_mapping_dict = {}
    with open(metadata_file_name) as metadata_file:
        for line in metadata_file:
            sp = line.strip().split("\t")
            str_date = sp[1]
            
            timestamp = np.datetime64(str_date)
            
            base_name = os.path.basename(sp[0])
            base_name_timestamp_mapping_dict[base_name] = timestamp
            
    # Loop through the documents, and collect topics for the documents. # Store in document_info, with "base_name" of the document as the key
    document_info = {}
    max_topic_confidence_for_topic = {}
    
    for el in obj["topic_model_output"]["documents"]:
        
        base_name = el["base_name"]
        filtered_labels = [l for l in el["additional_labels"] if l.replace(".", "").replace("-", "").replace(":", "").replace("T", "").isdigit()]
        if len(filtered_labels) == 0:
            print("No labels. You need to have a label (with a timestamp) to produce the timelines", el)
            exit()
         
        str_date = filtered_labels[0]
            
      
        timestamp = np.datetime64(str_date)
        
        # For each topic belonging to a document
        document_topics = []
        for t in el["document_topics"]:
            topic_info = {}
            topic_info["terms_found_in_text"] = t["terms_found_in_text"]
            topic_info["topic_index"] = t["topic_index"]
            topic_info["topic_confidence"] = t["topic_confidence"]
            #if len(topic_info["terms_found_in_text"]) > 1: # At least two terms included in text to include
            
            document_topics.append(topic_info)
            
            # Record information on max confidence for topic in max_topic_confidence_for_topic
            if topic_info["topic_index"] not in max_topic_confidence_for_topic:
                max_topic_confidence_for_topic[topic_info["topic_index"]] = topic_info["topic_confidence"]
            else:
                if topic_info["topic_confidence"] > max_topic_confidence_for_topic[topic_info["topic_index"]]:
                    max_topic_confidence_for_topic[topic_info["topic_index"]] = topic_info["topic_confidence"]
                                   
        document_info[base_name] = document_topics
    
    
    len_previous_row = None
    write_texts_topics = os.path.join(output_dir, file_name)
    
    with open(write_texts_topics, "w") as wtt:
  
        for base_name in sorted(base_name_timestamp_mapping_dict.keys()):
            document_row = [base_name] #filename
            document_row.append(str(base_name_timestamp_mapping_dict[base_name])) #timestamp
            
                        
            # Append topic confidence
            for topic_nr in sorted(show_to_user_nr_topic_index_mapping.keys()):
                topic_confidence = 0
                if base_name in document_info:
                    for topic_info in document_info[base_name]:
                        if topic_info['topic_index'] == topic_nr:
                            topic_confidence = topic_info['topic_confidence']
                document_row.append(str(topic_confidence))
                
            document_row.append("")
            # Append terms found in text
            for topic_nr in sorted(show_to_user_nr_topic_index_mapping.keys()):
                terms_found_in_text = ""
                if base_name in document_info:
                    for topic_info in document_info[base_name]:
                        if topic_info['topic_index'] == topic_nr:
                            terms_found_in_text = "/".join(topic_info['terms_found_in_text'])
                document_row.append(terms_found_in_text)
            
        
            if len_previous_row is None:
                len_previous_row = len(document_row)
                print("Nr of rows: ", len_previous_row)
            assert(len(document_row) == len_previous_row)
            wtt.write("\t".join(document_row) + "\n")
    
    

def write_topic_info(model_file, output_dir, translation_dict=None, label_length=20):

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        
    file_name = "labels_" + os.path.basename(model_file).replace(".json", ".txt")

    obj = None
    with open(model_file, 'r') as f:
        data = f.read()
        obj = json.loads(data)
    
    long_topic_names = []
    show_to_user_nr_topic_index_mapping = {}
    topic_list = obj["topic_model_output"]["topics"]

    for nr, (id, el) in enumerate(sorted([(el["id"], el) for el in topic_list])):
    
        topic_index = el["id"]
        show_to_user_nr_topic_index_mapping[topic_index] = nr
    
        terms = [t['term'] for t in el['topic_terms']]
        
        repr_terms = []
        for t in terms:
            
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
            #term_to_pick_as_rep = translation_dict[term_to_pick_as_rep.strip()]
        third_length = int(len(repr_terms)/3)

        topic_name_long = "\t".join(repr_terms)
        long_topic_names.append(topic_name_long)
            
        
    write_long_topic_names = os.path.join(output_dir, file_name)
    with open(write_long_topic_names, "w") as wltn:
        for el in long_topic_names:
            wltn.write(el + "\n")
            
    return show_to_user_nr_topic_index_mapping
    
    

