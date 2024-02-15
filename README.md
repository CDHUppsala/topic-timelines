topic-timelines
===============
This timeline visualisation visualises the occurrence of topics over time. It uses the output of the Topics2Themes tool, which extracts topics from a text corpus. The occurrence of these topics are visualised. 

To run the code, you therefore first need to run Topics2Themes on a text collection, and then run the code here on the output from this tool. You find Topics2Themes at: https://github.com/sprakradet

An example of how to run the code (and what is needed for configuring the Topics2Themes tool) is given in `plot_climate_timeline.py`. 

The code uses `numpy` and `matplotlib`.

The visualisation has been used for providing an overview of the content of several different types of corpora. The code is, however, still under development. The following examplifies the timeline visualisation on a corpus consisting of Swedish news about climate change.


![alttext](climate-news.png)

## Acknowledgements
The work on topic-timelines has mainly been conducted within the project ActDisease, partly with support from the research infrastructures InfraVis and Huminfra.

- [ActDisease](https://www.actdisease.org), Acting out Disease: How Patient Organizations Shaped Modern Medicine: ERC Starting Grant (ERC-2021-STG 101040999)
- [InfraVis](https://infravis.se), the Swedish National Research Infrastructure for Data Visualization: (Swedish Research Council, 2021-00181)
- [Huminfra](https://www.huminfra.se): National infrastructure for Research in the Humanities and Social Sciences (Swedish Research Council, 2021-00176)

