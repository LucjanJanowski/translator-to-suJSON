# translator-to-suJSON
A project aiming to create a set of tools for reading from non-standardised sources of subjectvie data
and converting this information to a standardised format called _suJSON_.

## An exemplary CSV file
[CCRIQ_Primary_Study_data_3labs.xlsx](CCRIQ_Primary_Study_data_3labs.xlsx) file includes exemplary
subjective data. Importantly, subjective scores are given using [the 5-level Absolute Category Rating (ACR) 
scale](https://en.wikipedia.org/wiki/Absolute_Category_Rating). 
For a time being, we are insterested only in the first  sheet from the file (the one named “Primary Study”). 
The goal is to extract as much information as possible. 

This file comes from a special type of a subjective experiment. A scene (e.g. a countryside landscape) 
represents Source Reference Sequence (SRC), whereas a type of a camera used can be thought of as 
Hypothetical Reference Circuit (HRC). Correspondingly, a scene shot using a given camera creates 
Processed Video Sequence (PVS). 

For a gentle introduction into a topic of subjective testing for video, please take a look at [this Wikipedia
page](https://en.wikipedia.org/wiki/Subjective_video_quality).

For more details about a classical design of a subjective test for video, one is encouraged to take a look 
at chapter 4 "DESIGN OVERVIEW: SUBJECTIVE EVALUATION PROCEDURE" in [a report from the VQEG HDTV Phase I
subjective test](https://www.its.bldrdoc.gov/media/4212/vqeg_hdtv_final_report_version_2.0.zip).

Should you have any questions please do not hesitate to contact Jakub Nawała.