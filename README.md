# translator-to-suJSON
A project aiming to create a set of tools for reading from non-standardised sources of subjectvie data
and converting this information to a standardised format called _suJSON_.

## Exemplary CSV files
There are two CSV-like files here. Both represent typical subjective tests for video. One is
[CCRIQ_Primary_Study_data_3labs.xlsx](CCRIQ_Primary_Study_data_3labs.xlsx) and the other is
[VQEG_HDTV_Final_Report_Data.xls](VQEG_HDTV_Final_Report_Data.xls). Their descriptions are provided
in the next paragraphs.

### CCRIQ
The [CCRIQ_Primary_Study_data_3labs.xlsx](CCRIQ_Primary_Study_data_3labs.xlsx) file includes exemplary
subjective data. Importantly, subjective scores are given using [the 5-level Absolute Category Rating (ACR) 
scale](https://en.wikipedia.org/wiki/Absolute_Category_Rating). 
For a time being, we are insterested only in the first  sheet from the file (the one named “Primary Study”). 
The goal is to extract as much information as possible. 

This file comes from a special type of a subjective experiment. A scene (e.g. a countryside landscape) 
represents Source Reference Circuit (SRC), whereas a type of a camera used can be thought of as 
Hypothetical Reference Circuit (HRC). Correspondingly, a scene shot using a given camera creates 
Processed Video Sequence (PVS).

### HDTV
The [VQEG_HDTV_Final_Report_Data.xls](VQEG_HDTV_Final_Report_Data.xls) comes from a classical
subjective test for video. SRC represents a pristine video recording, which is processed using
a given HRC to produce a PVS.

For the purpose of this project, we are interested only in the "vqeghd1_raw" sheet from this file.

## Theory
For a gentle introduction into a topic of subjective testing for video, please take a look at [this Wikipedia
page](https://en.wikipedia.org/wiki/Subjective_video_quality).

For more details about a classical design of a subjective test for video, one is encouraged to take a look 
at chapter 4 "DESIGN OVERVIEW: SUBJECTIVE EVALUATION PROCEDURE" in [a report from the VQEG HDTV Phase I
subjective test](https://www.its.bldrdoc.gov/media/4212/vqeg_hdtv_final_report_version_2.0.zip).

## Packages
In this project we are using the following packages: Pandas, NumPy

Should you have any questions please do not hesitate to contact Jakub Nawała.
