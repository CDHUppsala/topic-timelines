topic-timelines
===============
This timeline visualises the prevalence of topics over time. It uses the output of the Topics2Themes tool, which automatically extracts topics from a text corpus. 

To run the code, you therefore first need to run Topics2Themes on a text collection, and then run the code here on the output from this tool. You find Topics2Themes at: https://github.com/sprakradet

An example of how to run the code (and what is needed for configuring the Topics2Themes tool) is given in `plot_climate_timeline.py`. 

The code uses `numpy` and `matplotlib`.

The visualisation has been used for providing an overview of the content of several different types of corpora. The code is, however, still under development. The following examplifies the timeline visualisation for a corpus consisting of Swedish news about climate change. The y-axis shows the 39 topics that were automatically extracted from the corpus and the x-axis shows the date associated with the texts in the corpus. Each text is represented by a vertical line. The circles represent the level of association between the topic and the text. The larger the circle, the closer the association. Many overlapping circles at a certain date indicates that many texts on this topic were published this date. 

![A visualisation of climate news](climate-news.png)

It is possible to associate a unique hyperlink to each text that has been used for generating the timeline. The circles then become clickable links, which direct you to the web page associated with the text, for instance a web page that contains the text with its original layout. It is thereby possible to use the visualisation as a tool for locating and selecting potentially interesting texts for close reading.

![An example of zooming in and clicking](zoom-in.png)

## Acknowledgements
The work on topic-timelines has mainly been conducted within the project ActDisease, partly with support from the research infrastructures InfraVis and Huminfra.

- [ActDisease](https://www.actdisease.org): Acting out Disease: How Patient Organizations Shaped Modern Medicine: ERC Starting Grant (ERC-2021-STG 101040999)
- [InfraVis](https://infravis.se): the Swedish National Research Infrastructure for Data Visualization (Swedish Research Council, 2021-00181)
- [Huminfra](https://www.huminfra.se): National infrastructure for Research in the Humanities and Social Sciences (Swedish Research Council, 2021-00176)

