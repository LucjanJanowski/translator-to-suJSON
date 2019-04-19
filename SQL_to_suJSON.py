import json
import numpy as np
import mysql.connector


# TODO If you introduce new IDs for PVSs, use a dictionary to map old IDs into new ones

# Function to resolve numpy type problem
def default(o):
    if isinstance(o, np.int64):
        return int(o)
    # raise TypeError


# Function to writing results into json file
def write_to_json_file(path, file_name, data):
    file_path_name_wext = './' + path + './' + file_name + '.json'
    with open(file_path_name_wext, 'w') as fp:
        json.dump(data, fp, indent=2, default=default)


# Main function
def main():
    # Open configuration file
    with open('config.json') as experiment_description:
        ed = json.load(experiment_description)

    cnx = mysql.connector.connect(
        user='root',
        password='root',
        host='localhost',
        database='sujson')

    cursor = cnx.cursor()

    # Define result file path
    path = './'

    # Define result file name
    file_name = 'result_from_SQL'

    # Fetch DATASET_NAME from description file
    dataset_name = ed['dataset_name']

    # suJSON_VERSION
    sujson_version = '1.1-in_progress'

    # Fetch CHARACTERISTICS from description file
    characteristics = ed['characteristics']

    # Fetch TASKS from description file
    tasks = ed['tasks']

    # Fetch SCALES from description file
    scales = ed['scales']

    # Fetch QUESTIONS from description file
    questions = ed['questions']

    # Define structure of final json file
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

    # Fetch a list of PVSs from the SQL database
    query = '''SELECT ID, FILE_PATH FROM TESTS_FILE'''
    cursor.execute(query)
    for (filepath_id, filepath) in cursor:
        final_data['pvs'].append({'id': filepath_id,
                                  'src_id': None,
                                  'hrc_id': None,
                                  'file_path': filepath[:-1]})

    # Fetch a list of SUBJECTS from the SQL database
    query = '''SELECT ID FROM USER'''
    cursor.execute(query)
    for subject_id in cursor:
        final_data['subjects'].append({'id': subject_id[0]})

    # Fetch a list of TRIALS from the SQL database
    query = '''SELECT ID, ID_USER, ID_FILE FROM RESULTS'''
    cursor.execute(query)
    for (trial_id, subject_id, pvs_id) in cursor:
        final_data['trials'].append({'id': trial_id,
                                     'subject_id': subject_id,
                                     'task_id': None,
                                     'pvs_id': pvs_id})

    # Fetch a list of SCORES from the SQL database
    # TODO Make a connection with correct trials objects
    # TODO Make a connection with a correct question object
    query = '''SELECT ID, ID_FILE, MOS FROM RESULTS'''
    cursor.execute(query)
    for (ind, (result_id, pvs_id, score)) in enumerate(cursor):
        final_data['scores'].append({'id': ind,
                                     'question_id': None,
                                     'pvs_id': pvs_id,
                                     'score': score})

    cursor.close()
    cnx.close()

    # Save results to json file
    write_to_json_file(path, file_name, final_data)


if __name__ == '__main__':
    main()
