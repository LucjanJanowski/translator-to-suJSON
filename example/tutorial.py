from sujson._sujson import Sujson
import subprocess
from subprocess import PIPE
from pathlib import Path

sujson = Sujson()
sujson_file = str(Path('example', 'hdtv5.json'))
sujson._read_sujson(sujson_file)
df = sujson.pandas_export()
print(df)

# mean
print(df.groupby('stimulus_id')['score'].mean())
# standard deviation
print(df.groupby('stimulus_id')['score'].std())


# translating .xls file to suJSON
xls_file = str(Path('example', 'data', 'VQEG_HDTV_Final_Report_Data.xls'))
config = str(Path('example', 'config', 'config_for_hdtv.json'))
sujson_from_xls = str(Path('example', 'xls_output.json'))

command = 'python -m sujson ingest {} {} -o {}'.format(xls_file, config, sujson_from_xls)
proc = subprocess.Popen(command, stdin=PIPE, stderr=PIPE, text=True)
proc.communicate()


# translating .xls file to suJSON without  output file - printing to console
command = 'python -m sujson ingest {} {}'.format(xls_file, config)
proc = subprocess.Popen(command, stdin=PIPE, stderr=PIPE, text=True)
proc.communicate()


# translating .csv file to suJSON
xls_file = str(Path('example', 'data', 'subjective_quality_datasets.csv'))
config = str(Path('example', 'config', 'config_for_hdtv_csv.json'))
sujson_from_csv = str(Path('example', 'csv_output.json'))

command = 'python -m sujson ingest {} {} -o {}'.format(xls_file, config, sujson_from_csv)
proc = subprocess.Popen(command, stdin=PIPE, stderr=PIPE, text=True)
proc.communicate()


# translating .csv file to suJSON without  output file - printing to console
command = 'python -m sujson ingest {} {}'.format(xls_file, config)
proc = subprocess.Popen(command, stdin=PIPE, stderr=PIPE, text=True)
proc.communicate()


# suJSON to pandas dataframe (.csv)
output_csv = str(Path('example', 'output_pandas.csv'))
export_format = 'Pandas'

command = 'python -m sujson export {} -o {} -f {}'.format(sujson_from_csv, output_csv, export_format)
proc = subprocess.Popen(command, stdin=PIPE, stderr=PIPE, text=True)
proc.communicate()


# suJSON to .pickle file
output_pickle = str(Path('example', 'output_pickle.pickle'))
export_format = 'suJSON'

command = 'python -m sujson export {} -o {} -f {}'.format(sujson_from_csv, output_pickle, export_format)
proc = subprocess.Popen(command, stdin=PIPE, stderr=PIPE, text=True)
proc.communicate()
