# suJSON

A project aiming to create a set of tools for reading from non-standardised sources of subjectvie data and converting this information to a standardised format called _suJSON_.

## Scripts

### Requirements

- Python 3
- `pip3 install --user .`

### Usage

The `sujson` command has two subcommands:

- `ingest`: Ingest a file (XLS or CSV)
- `export`: Export suJSON to CSV

```
positional arguments:
  {ingest,export}

optional arguments:
  -h, --help       show this help message and exit
  -f, --force      Force overwrite existing files
  -d, --debug      Print debugging output
  -v, --verbose    Print verbose output
  -n, --dry-run    Do not run, only print what would be done
  --version        Print version and exit
```

For ingesting:

```
positional arguments:
  input                 Input file, currently only .xslx or .csv supported

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config file
  -o OUTPUT, --output OUTPUT
                        Output file, currently only .json supported. If not
                        given, will write to STDOUT.
```

For exporting:

```
positional arguments:
  input                 Input suJSON file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file, currently only .csv supported. If not
                        given, will write to STDOUT.
```

## Examples

For example, run:

```
python3 -m sujson ingest example/data/its4s_subjective_data.xlsx -c example/config/config.json.for_its4s.json
```

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

## Exemplary MySQL dump

The [subjective_scores_for_suJSON.sql](subjective_scores_for_suJSON.sql) file contains an exemplary
dump from a MySQL database. In this case, the source MySQL database is designed to aid subjective 
testing. It is used to store results on-the-fly. Those are later analysed to draw conclusions. It
is assumed that architecture of this database reflects typical architectures of databases
dedicated to subjective testing.

The database consists of eight (8) tables, namely:
1. QUESTIONNAIRE_ANSWERS,
2. QUESTIONS,
3. RESULTS,
4. SCREEN,
5. SLIDER_RESULTS,
6. TESTS_DOC,
7. TESTS_FILE,
8. USER.

Each of those serves a certain purpose. To make this description brief, only three (3) most important
ones are described in details (please see the table below).

| Table | Description |
| ----- | ----------- |
| RESULTS | Each row represents a score given by a single tester (identified by ID_USER) to a single image (identified by ID_FILE). Scores are placed in the MOS column (yes, "MOS" is not the most fortunate name for the column with individual scores). |
| TESTS_FILE | Each row represents a single image. The ID column here corresponds to the ID_FILE column in the RESULTS table. The FILE_PATH column specifies the location of each image. Note that locations of files are specific to a server hosting this database. |
| USER | Each row represents a single tester. The ID column here corresponds to the ID_USER column in the RESULTS table. |

## Theory
For a gentle introduction into a topic of subjective testing for video, please take a look at [this Wikipedia
page](https://en.wikipedia.org/wiki/Subjective_video_quality).

For more details about a classical design of a subjective test for video, one is encouraged to take a look 
at chapter 4 "DESIGN OVERVIEW: SUBJECTIVE EVALUATION PROCEDURE" in [a report from the VQEG HDTV Phase I
subjective test](https://www.its.bldrdoc.gov/media/4212/vqeg_hdtv_final_report_version_2.0.zip).

## Authors/Contact

Should you have any questions please do not hesitate to contact the authors.

Authors:

- Jakub Nawała
- Werner Robitza
