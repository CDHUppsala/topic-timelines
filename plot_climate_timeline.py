import plot_timeline

def plot_climate():
    # These two are output files from Topics2Themes:
    # https://github.com/sprakradet/topics2themes
    model_file = "/Users/marsk757/topics2themes/topics2themes/data_folder/climate-news/topics2themes_exports_folder_created_by_system/644aca8c54cac60d53accbd7_model.json"
    metadata_file_name = "/Users/marsk757/topics2themes/topics2themes/data_folder/climate-news/topics2themes_exports_folder_created_by_system/all_files.csv"
    
    # Topics2Themes needs to be configured to use the
    # the ADDITIONAL_LABELS_METHOD, and to let that one
    # return exact ONE label, which is the date with which a document is associated
    #
    """
    ADDITIONAL_LABELS_METHOD = get_labels
    def get_labels(doc_path):
        base_name = os.path.basename(doc_path)
        date_str = base_name[:10]
        labels = []
        labels.append(date_str)
        return labels
    """
    
    outputdir = "plots"
    file_name = "climate-news"
    add_for_coliding_dates = False
    label_length = 40
    circle_scale_factor=1000
    bar_width = 0.01
    bar_transparency=0.3
    hours_between_label_dates=1
    
    plot_timeline.make_plot(model_file, outputdir, metadata_file_name, file_name, add_for_coliding_dates, label_length=label_length, circle_scale_factor=circle_scale_factor, bar_width=bar_width, bar_transparency=bar_transparency, hours_between_label_dates=hours_between_label_dates)

plot_climate()
