Topic Timelines
===============
This timeline visualises the prevalence of topics over time in a temporally extende corpus, as well as the prominence of the topics in the texts. 

The following examplifies the timeline visualisation for a corpus consisting of Swedish news about diabetes. The y-axis shows the 24 topics that were automatically extracted from the corpus and the x-axis shows the date associated with the texts in the corpus. Each text is represented by a vertical line. The circles represent the level of association between the topic and the text. The larger the circle, the closer the association. Many overlapping circles at a certain date indicates that many texts on this topic were published this date. 

![A visualisation of news on diabeted](diabetes.png)

It is possible to associate a unique hyperlink to each text that has been used for generating the timeline. The circles then become clickable links, which direct you to the web page associated with the text, for instance a web page that contains the text with its original layout. It is thereby possible to use the visualisation as a tool for locating and selecting potentially interesting texts for close reading.

![An example of zooming in and clicking](zoom_in.png)

Here is a demo page of a clickable timeline: (https://cdhuppsala.github.io/topic-timelines-examples/diabetes_popup.html)

To create the visualisation, two topic modelling output files are needed, as shown in ![diabetes](diabetes). In addition to output from topic modelling, the files to visualised also need an associated timestamp, e.g., publication date. The output files can, for instance, be created from the output of the topic modelling tool Topics2Themes, but running the script ![transform_topics2themes_to_topictimelines.py](transform_topics2themes_to_topictimelines.py)

Topics2Themes
-------------
The Topics2Themes tool, which automatically extracts topics from a text corpus. To connect it to the output of Topics2Themes, you need this tool, which you can find at: [https://github.com/mariask2/topics2themes](https://github.com/mariask2/topics2themes)

An example of how to run the code (and what is needed for configuring the Topics2Themes tool in order to be able to create timelines) is given in ![example-topics2themes-configuration](example-topics2themes-configuration). 

Dependencies
-------------

The code uses `numpy` and `matplotlib`.


Acknowledgements
----------------
The work on topic-timelines has mainly been conducted within the project ActDisease, partly with support from the research infrastructures InfraVis and Huminfra.

- [ActDisease](https://www.actdisease.org): Acting out Disease: How Patient Organizations Shaped Modern Medicine: ERC Starting Grant (ERC-2021-STG 101040999)
- [InfraVis](https://infravis.se): the Swedish National Research Infrastructure for Data Visualization (Swedish Research Council, 2021-00181)
- [Huminfra](https://www.huminfra.se): National infrastructure for Research in the Humanities and Social Sciences (Swedish Research Council, 2021-00176)

