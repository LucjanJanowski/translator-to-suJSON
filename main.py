import pandas as pd
import json
import numpy as np


def default(o):
    if isinstance(o, np.int64): return int(o)
    raise TypeError


def write_to_json_file(path, file_name, data):
    file_path_name_wext = './' + path + './' + file_name + '.json'
    with open(file_path_name_wext, 'w') as fp:
        json.dump(data, fp, indent=2, default=default)


wb = pd.read_excel('VQEG_HDTV_Final_Report_Data.xls',
                   sheet_name='vqeghd1_raw')
desc = open('experiment_description.txt', 'r+')


# TODO: When provided in the configuration file, read what are the names of columns to read data from
# for example: what is the name of the columns storing SRCs numbers?

src_num = wb['SRC Num'].unique()
hrc_num = wb['HRC Num'].unique()
pvs = wb.File.unique()

path = './'
file_name = 'result'

# DATASET_NAME
dataset_name = 'vqeghd1'

# SUJSON_VERSION
sujson_version = '1.1-in_progress'

# CHARACTERISTICS
characteristics = 'charakterystyka'

final_data = {'dataset_name': dataset_name,
              'sujson_version': sujson_version,
              'characteristics': characteristics,
              'tasks': [],
              'scales': [],
              'questions': [],
              'src': [],
              'hrc': [],
              'pvs': [],
              'subjects': [],
              'trials': [],
              'scores': []}

# SCALES

# QUESTIONS
id_num = 1
final_data['questions'].append({'id': id_num})

# TASKS
id_num = 1
final_data['tasks'].append({'id': id_num})

# SRC
id_num = 1
for i in src_num:
    if i <= 9:
        a = '0' + str(i)
    else:
        a = str(i)
    final_data['src'].append({'id': id_num,
                              'name': dataset_name + '_src' + a})
    id_num = id_num + 1

# HRC
id_num = 1
for i in hrc_num:
    if i <= 9:
        a = '0' + str(i)
    else:
        a = str(i)
    final_data['hrc'].append({'id': id_num,
                              'name': dataset_name + '_hrc' + a})
    id_num = id_num + 1

# PVS
id_num = 1
m = 0
for i in src_num:
    if i <= 9:
        a = '0' + str(i)
    else:
        a = str(i)
    src_id = final_data['src'][m]['id']
    m = m + 1
    n = 0
    for j in hrc_num:
        if j <= 9:
            b = '0' + str(j)
        else:
            b = str(j)
        hrc_id = final_data['hrc'][n]['id']
        n = n + 1
        for element in pvs:
            valid_name = dataset_name + '_src' + a + '_hrc' + b
            if element.startswith(valid_name):
                final_data['pvs'].append({'id': id_num,
                                          'src_id': src_id,
                                          'hrc_id': hrc_id,
                                          # 'file_check_name': dataset_name + '_src' + a + '_hrc' + b,
                                          'file_name': element})
                id_num = id_num + 1

# SUBJECTS
for subjects in list(wb):
    if isinstance(subjects, int):
        final_data['subjects'].append({'id': subjects})

# TRIALS
id_num = 1
subject_num = 0
for subject_id in final_data['subjects']:
    subject_id_num = final_data['subjects'][subject_num]['id']
    subject_num = subject_num + 1
    task_num = 0
    for task_id in final_data['tasks']:
        task_id_num = final_data['tasks'][task_num]['id']
        task_num = task_num + 1
        pvs_num = 0
        for pvs_id in final_data['pvs']:
            pvs_id_num = final_data['pvs'][pvs_num]['id']
            pvs_num = pvs_num + 1
            final_data['trials'].append({'id': id_num,
                                         'subject_id': subject_id_num,
                                         'task_id': task_id_num,
                                         'pvs_id': pvs_id_num,
                                         'score_id': id_num})
            id_num = id_num + 1

# SCORES
id_num = 1
score_num = 0
for score_id in final_data['trials']:
    pvs_id_num = final_data['trials'][score_num]['pvs_id']
    subject_id_num = final_data['trials'][score_num]['subject_id']
    subject_score = wb[subject_id_num][pvs_id_num - 1]
    score_num = score_num + 1
    question_num = 0
    for question_id in final_data['questions']:
        question_id_num = final_data['questions'][question_num]['id']
        question_num = question_num + 1
        final_data['scores'].append({'id': id_num,
                                     'question_id': question_id_num,
                                     'pvs_id': pvs_id_num,
                                     'score': subject_score})
        id_num = id_num + 1

write_to_json_file(path, file_name, final_data)
