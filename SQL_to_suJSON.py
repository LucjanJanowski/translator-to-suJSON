import json
import numpy as np
import mysql.connector

db = mysql.connector.connect(
    user='root',
    password='root',
    host='localhost',
    database='sujson')

cursor = db.cursor()


def default(o):                                                       # resolve numpy type problem
    if isinstance(o, np.int64):
        return int(o)
    # raise TypeError


def write_to_json_file(path, file_name, data):                        # write to json file function
    file_path_name_wext = './' + path + './' + file_name + '.json'
    with open(file_path_name_wext, 'w') as fp:
        json.dump(data, fp, indent=2, default=default)


with open('config.json') as experiment_description:                   # open configuration file
    ed = json.load(experiment_description)


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

# SCORES
cursor.execute('SELECT ID, ID_USER, ID_FILE, ID_TEST, TEST_DATE FROM results')
result = cursor.fetchall()
for (id, subject_id,  pvs_id, test_id, test_date) in result:
    final_data['scores'].append({'id': id,
                                 'subject_id': subject_id,
                                 'task_id': None,
                                 'pvs_id': pvs_id,
                                 'test_id': test_id,
                                 'test_date': test_date})

write_to_json_file(path, file_name, final_data)                       # save results to json file
