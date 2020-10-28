from sujson._sujson import Sujson
import os

# TODO @awro1444 Ideally, everything that we need to use here should be available in the repo. In other words, please
#  make the code more portable
sujson = Sujson()
sujson_file = 'D:\\translator-to-suJSON-master\hdtv1.json'
sujson._read_sujson(sujson_file)
df = sujson.pandas_export()
print(df)

# mean
print(df.groupby('stimulus_id')['score'].mean())

# standard deviation
print(df.groupby('stimulus_id')['score'].std())


# tutorial

# translating .xml file to suJSON
# my_xls = 'D:\\Users\\awrob\GitHub\\translator-to-suJSON\example\data\VQEG_HDTV_Final_Report_Data.xls'
my_xls = 'example\data\VQEG_HDTV_Final_Report_Data.xls'
config = 'example\config\config_for_hdtv.json'
output_sujson = 'D:\\translator-to-suJSON-master\pandas\output.json'

os.system('python -m sujson ingest {} -c {} -o {}'.format(my_xls, config, output_sujson))

# suJSON to pandas dataframe (.csv)
output_csv = 'D:\\translator-to-suJSON-master\pandas\output_pandas.csv'
export_format = 'Pandas'
os.system('python -m sujson export {} -o {} -f {}'.format(output_sujson, output_csv, export_format))

# suJSON to .pickle file
output_pickle = 'D:\\translator-to-suJSON-master\pandas\output_pickle.pickle'
export_format = 'suJSON'
os.system('python -m sujson export {} -o {} -f {}'.format(output_sujson, output_pickle, export_format))
