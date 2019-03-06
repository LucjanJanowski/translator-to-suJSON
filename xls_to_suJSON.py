import pandas as pd
import json
import numpy as np


def default(o):
    """
    Function which returns a serializable object for o
    :param o: Given valuable
    :return: A serializable object for o
    """
    if isinstance(o, np.int64):
        return int(o)
    raise TypeError


def write_to_json_file(path, file_name, data):
    """
    Function which allows saving to JSON file with defined name as well as file path
    :param path: Define result file path
    :param file_name: File name
    :param data: Data to save
    :return: Final JSON file with data saved in specified path
    """
    file_path_name_wext = './' + path + './' + file_name + '.json'
    with open(file_path_name_wext, 'w') as fp:
        json.dump(data, fp, indent=2, default=default)


# Open configuration file
with open('config.json') as configuration_file:
    cf = json.load(configuration_file)

# Open xls file with data
wb = pd.read_excel(cf['file_name'],
                   sheet_name=cf['sheet_hdr_name'],
                   header=cf['header_row_pos'],
                   skipfooter=cf["footer_rows_to_skip"])

# Create list of unique src
src_num = wb[cf['src_hdr_name']].unique()

# Create list of unique hrc
hrc_num = wb[cf['hrc_hdr_name']].unique()

# Create list of unique pvs
# NOTE: The value given in the configuration file must exactly match header content in the analysed file
pvs = wb[cf['file_hdr_name']].unique()

# Define result file path
path = cf['result_file_path']

# Define result file name
file_name = cf['result_file_name']

# DATASET_NAME
dataset_name = cf['dataset_name']

# SUJSON_VERSION
sujson_version = '1.1-in_progress'

# CHARACTERISTICS
characteristics = cf['characteristics']

# TASKS
tasks = cf['tasks']

# SCALES
scales = cf['scales']

# QUESTIONS
questions = cf['questions']

# Define structure of final JSON file
final_data = {'dataset_name': dataset_name,
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

# TODO: Create new SRC, HRC, PVS name writing system

# Create SRC list for final_data
for (ind, value) in enumerate(src_num):
    id_num_str = "{:02d}".format(ind+1)

    # Add to final_data list of src
    final_data['src'].append({'id': ind,
                              'name': dataset_name + '_src' + id_num_str})

# Create HRC list for final_data
for (ind, value) in enumerate(hrc_num):
    id_num_str = "{:02d}".format(ind+1)

    # Add to final_data list of hrc
    final_data['hrc'].append({'id': ind,
                              'name': dataset_name + '_hrc' + id_num_str})  # Name is optional

# Create PVS list for final_data
# TODO: Find better solution for creating PVS list with a correct name (considering SRC and HRC)

# m = 0
# for (src_ind, src_value) in enumerate(src_num):
#     src_id_num_str = "{:02d}".format(src_ind+1)
#
#     # Take id of m element from src list
#     src_id = final_data['src'][m]['id']
#     m = m + 1
#     n = 0
#     for (hrc_ind, hrc_value) in enumerate(hrc_num):
#         hrc_id_num_str = "{:02d}".format(hrc_ind+1)
#
#         # Take id of n element from hrc list
#         hrc_id = final_data['hrc'][n]['id']
#         n = n + 1
id_num = 1
for element in pvs:
    # Add to final_data list of pvs
    final_data['pvs'].append({'id': id_num,
                              # 'src_id': src_id,
                              # 'hrc_id': hrc_id,
                              'file_name': element})    # NOTE: In the original suJSON this field is
    #  called "path"
    id_num = id_num + 1

# SUBJECTS
# Take column header number of the first subject
subject_start_num = cf['score_column_range']['start']

# Take column header number of the last subject
subject_finish_num = cf['score_column_range']['stop']

subjects = 1
for i in range(subject_start_num, subject_finish_num+1):
    # Add to final_data list of subjects
    final_data['subjects'].append({'id': subjects})
    subjects += 1

# TRIALS
id_num = 1
subject_num = 0
for subject_id in final_data['subjects']:
    # Take id from subjects list
    subject_id_num = final_data['subjects'][subject_num]['id']
    subject_num = subject_num + 1
    task_num = 0
    for task_id in final_data['tasks']:
        # Take id from tasks list
        task_id_num = final_data['tasks'][task_num]['id']
        task_num = task_num + 1
        pvs_num = 0
        for pvs_id in final_data['pvs']:
            # Take id from pvs list
            pvs_id_num = final_data['pvs'][pvs_num]['id']
            pvs_num = pvs_num + 1
            # Add to final_data list of trials
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
    # Take pvs_id from trials list
    pvs_id_num = final_data['trials'][score_num]['pvs_id']
    # Take subject_id from trials list
    subject_id_num = final_data['trials'][score_num]['subject_id']
    subject_id_num = subject_id_num + subject_start_num - 2
    # Take subject score from dataframe
    subject_score = wb[wb.columns[subject_id_num]][pvs_id_num - 1]
    score_num = score_num + 1
    question_num = 0
    for question_id in final_data['questions']:
        # Take id from questions list
        question_id_num = final_data['questions'][question_num]['id']
        question_num = question_num + 1
        # Add to final_data list of scores
        final_data['scores'].append({'id': id_num,
                                     'question_id': question_id_num,
                                     'pvs_id': pvs_id_num,
                                     'score': subject_score})
        id_num = id_num + 1

# Save results to JSON file
write_to_json_file(path, file_name, final_data)
