import pandas as pd

my_file = "D:\\translator-to-suJSON-master\pandas\hdtv1.csv"

data_frame = pd.read_csv(my_file)
print(data_frame.groupby('stimulus_id')['score'].mean())
print(data_frame.groupby('stimulus_id')['score'].std())