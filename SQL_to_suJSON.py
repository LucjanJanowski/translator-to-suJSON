import pandas as pd
import json
import numpy as np
import mysql.connector

db = mysql.connector.connect(
    user='root',
    password='root',
    host='localhost',
    database='sujson'
)

cursor = db.cursor()


def default(o):                                                       # resolve numpy type problem
    if isinstance(o, np.int64):
        return int(o)
    #raise TypeError


def write_to_json_file(path, file_name, data):                        # write to json file function
    file_path_name_wext = './' + path + './' + file_name + '.json'
    with open(file_path_name_wext, 'w') as fp:
        json.dump(data, fp, indent=2, default=default)


with open('config.json') as experiment_description:                   # open configuration file
    ed = json.load(experiment_description)

'''wb = pd.read_excel(ed['file_name'],                                   # open xls file with data
                   sheet_name=ed['sheet_hdr_name'],
                   header=ed['header_row_pos'])

src_num = wb[ed['src_hdr_name']].unique()                             # create list of src
hrc_num = wb[ed['hrc_hdr_name']].unique()                             # create list of hrc
pvs = wb[ed['file_hdr_name']].unique()                                # create list of pvs
'''

path = './'                                                           # define result file path
file_name = 'result'                                                  # define result file name

# DATASET_NAME
dataset_name = ed['dataset_name']

# SUJSON_VERSION
sujson_version = '1.1-in_progress'

# CHARACTERISTICS
characteristics = ed['characteristics']

# TASKS
tasks = ed['tasks']

# SCALES
scales = ed['scales']

# QUESTIONS
questions = ed['questions']

final_data = {'dataset_name': dataset_name,                           # define structure of final json file
              'sujson_version': sujson_version,
              'characteristics': characteristics,
              'tasks': tasks,
              'scales': scales,
              'questions': questions,
              'src': [],
              'hrc': [],
              'pvs': [],
              'subjects': [],
              'trials': [],
              'scores': []}

'''# SRC
id_num = 1
for i in src_num:                                                     # iterate over every element from src_num list
    if i <= 9:
        a = '0' + str(i)
    else:
        a = str(i)
    final_data['src'].append({'id': id_num,                           # add to final data list of src
                              'name': dataset_name + '_src' + a})
    id_num = id_num + 1

# HRC
id_num = 1
for i in hrc_num:                                                     # iterate over every element from hrc_num list
    if i <= 9:
        a = '0' + str(i)
    else:
        a = str(i)
    final_data['hrc'].append({'id': id_num,                           # add to final data list of hrc
                              'name': dataset_name + '_hrc' + a})
    id_num = id_num + 1
'''

# PVS

cursor.execute('SELECT ID, FILE_PATH FROM tests_file')
result = cursor.fetchall()

for (id, filepath) in result:
    final_data['pvs'].append({'id': id,
                              'src_id': None,
                              'hrc_id': None,
                              'file_path': filepath})




# SUBJECTS
cursor.execute('SELECT ID FROM user')
subjects = cursor.fetchall()

for id in subjects:
    final_data['subjects'].append({'id': id})



# TRIALS
cursor.execute('SELECT ID, ID_USER, ID_FILE, ID_TEST, TEST_DATE FROM results')
result = cursor.fetchall()
for (id, subject_id,  pvs_id, test_id, test_date) in result:
    final_data['trials'].append({'id': id,
                                 'subject_id': subject_id,
                                 'task_id': None,
                                 'pvs_id': pvs_id,
                                 'test_id': test_id,
                                 'test_date': test_date})



'''
# SCORES
id_num = 1
score_num = 0
for score_id in final_data['trials']:                                 # iterate over every element from trials
    pvs_id_num = final_data['trials'][score_num]['pvs_id']            # take pvs id from trials list
    subject_id_num = final_data['trials'][score_num]['subject_id']    # take subject id from trials list
    subject_score = wb[subject_id_num][pvs_id_num - 1]
    score_num = score_num + 1
    question_num = 0
    for question_id in final_data['questions']:                       # iterate over every element from questions
        question_id_num = final_data['questions'][question_num]['id'] # take id from questions list
        question_num = question_num + 1
        final_data['scores'].append({'id': id_num,                    # add to final data list of scores
                                     'question_id': question_id_num,
                                     'pvs_id': pvs_id_num,
                                     'score': subject_score})
        id_num = id_num + 1
'''
write_to_json_file(path, file_name, final_data)                       # save results to json file