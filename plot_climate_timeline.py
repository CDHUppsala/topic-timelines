import plot_timeline


def plot_climate():
    model_file = "topics2themes/data_folder/climate-news/topics2themes_exports_folder_created_by_system/644aca8c54cac60d53accbd7_model.json"
    metadata_file_name = "topics2themes/data_folder/climate-news/topics2themes_exports_folder_created_by_system/all_files.csv"
    outputdir = "plots"
    file_name = "climate-news.pdf"
    add_for_coliding_dates = False
    label_length = 20
    log = True
    
    plot_timeline.make_plot(model_file, outputdir, metadata_file_name, file_name, add_for_coliding_dates, label_length, log=log)

plot_climate()
