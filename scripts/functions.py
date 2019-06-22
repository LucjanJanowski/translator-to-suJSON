def json_structure(cf):
    """
    Definition of json structure and create final data for output file
    :param cf: Configuration file
    :return: final_data structure for output json file
    """
    # DATASET_NAME
    dataset_name = cf['dataset_name']

    # SUJSON_VERSION
    sujson_version = '1.5-in_progress'

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

    return final_data


def pvs_id_list(wb, cf, pvs_unique, final_data):
    """
    Additional function which creates list of id for every data file row
    :param wb: Data file
    :param cf: Configuration file
    :param pvs_unique:
    :param final_data: Final data structure
    :return: List of id for every data row
    """
    pvs_list = []
    pvs_list_id = []
    for helper_ind, row in wb.iterrows():
        for ind, val in enumerate(pvs_unique):
            if row[cf['src_hdr_name']] == val[1] and row[cf['hrc_hdr_name']] == val[2]:
                pvs_list.append(val[0])
    for helper_ind, id in enumerate(pvs_list):
        for ind, val in enumerate(final_data['pvs']):
            if val['file_name'] == id:
                pvs_list_id.append(val['id'])
    return pvs_list_id


def subject_tidy(wb, cf, final_data):
    """
    Function which adds subjects list to final_data for tidy data
    :param wb: Data file
    :param cf: Configuration file
    :param final_data: Final data structure
    :return: Adds subjects to final_data structure
    """
    subjects = wb[cf['subject_column_name']].unique()
    for subject, val in enumerate(subjects):
        # Add to final_data list of src
        final_data['subjects'].append({'id': subject + 1,
                                       'name': val})


def subject_no_tidy(cf, final_data):
    """
    Function which adds subjects list to final_data for non tidy data
    :param cf: Configuration file
    :param final_data: Final data structure
    :return: Adds subjects to final_data structure
    """
    # Define subject scores column range
    # Take column header number of first subject
    subject_start_num = cf['score_column_range']['start']

    # Take column header number of last subject
    subject_finish_num = cf['score_column_range']['stop']

    for subject, val in enumerate(range(subject_start_num, subject_finish_num + 1)):
        # Add to final_data list of subjects
        final_data['subjects'].append({'id': subject + 1})


def pvs_unique_data(wb, cf):
    """
    Additional function which creates list of unique pvs
    :param wb: Data file
    :param cf: Configuration file
    :return: Unique list of pvs
    """
    pvs_unique = []
    used_name = []
    for helper_ind, row in wb.iterrows():
        if row[cf['src_hdr_name']] + "_" + row[cf['hrc_hdr_name']] not in used_name:
            pvs_unique.append((row[cf['src_hdr_name']] + "_" + row[cf['hrc_hdr_name']],
                               row[cf['src_hdr_name']],
                               row[cf['hrc_hdr_name']]))
            used_name.append(row[cf['src_hdr_name']] + "_" + row[cf['hrc_hdr_name']])
    return pvs_unique


def trials_tidy(wb, cf, final_data):
    """
    Function which adds trials to final_data for tidy data
    :param wb: Data file
    :param cf: Configuration file
    :param final_data: Final data structure
    :return: Adds trials to final_data structure
    """
    id_num = 1
    pvs_unique = pvs_unique_data(wb, cf)
    for task_num, task_id in enumerate(final_data['tasks']):
        # Take id from tasks list
        task_id_num = final_data['tasks'][task_num]['id']
        subjects = wb[cf['subject_column_name']]
        subjects_unique = wb[cf['subject_column_name']].unique()
        pvs_list = pvs_id_list(wb, cf, pvs_unique, final_data)
        for id, val in enumerate(subjects):
            for subject_id_num, subject_id in enumerate(subjects_unique):
                if val == subject_id:
                    final_data['trials'].append({'id': id_num,
                                                 'subject_id': subject_id_num + 1,
                                                 'task_id': task_id_num,
                                                 'pvs_id': pvs_list[id_num - 1],
                                                 'score_id': id_num})
                    id_num = id_num + 1


def trials_no_tidy(final_data):
    """
    Function which adds trials to final_data for non tidy data
    :param final_data: Final data structure
    :return: Adds trials to final_data structure
    """
    id_num = 1
    for subject_num, subject_id in enumerate(final_data['subjects']):
        # Take id from subjects list
        subject_id_num = final_data['subjects'][subject_num]['id']
        for task_num, task_id in enumerate(final_data['tasks']):
            # Take id from tasks list
            task_id_num = final_data['tasks'][task_num]['id']
            for pvs_num, pvs_id in enumerate(final_data['pvs']):
                # Take id from pvs list
                pvs_id_num = final_data['pvs'][pvs_num]['id']
                # Add to final_data list of trials
                final_data['trials'].append({'id': id_num,
                                             'subject_id': subject_id_num,
                                             'task_id': task_id_num,
                                             'pvs_id': pvs_id_num,
                                             'score_id': id_num})
                id_num = id_num + 1


def scores_tidy(wb, cf, final_data):
    """
    Function which adds scores to final_data for tidy data
    :param wb: Data file
    :param cf: Configuration file
    :param final_data: Final data structure
    :return: Adds trials to final_data structure
    """
    id_num = 1
    for score_num, score_id in enumerate(final_data['trials']):
        # Take pvs_id from trials list
        pvs_id_num = final_data['trials'][score_num]['pvs_id']
        # Take subject score from dataframe
        subject_score = wb[cf['score_column']][id_num - 1]
        for question_num, question_id in enumerate(final_data['questions']):
            # Take id from questions list
            question_id_num = final_data['questions'][question_num]['id']
            # Add to final_data list of scores
            final_data['scores'].append({'id': id_num,
                                         'question_id': question_id_num,
                                         'pvs_id': pvs_id_num,
                                         'score': subject_score})
            id_num = id_num + 1


def scores_no_tidy(wb, cf, final_data):
    """
    Function which adds scores to final_data for non tidy data
    :param wb: Data file
    :param cf: Configuration file
    :param final_data: Final data structure
    :return: Adds trials to final_data structure
    """
    # Take column header number of first subject
    subject_start_num = cf['score_column_range']['start']

    # Scores
    id_num = 1
    for score_num, score_id in enumerate(final_data['trials']):
        # Take pvs_id from trials list
        pvs_id_num = final_data['trials'][score_num]['pvs_id']
        # Take subject_id from trials list
        subject_id_num = final_data['trials'][score_num]['subject_id']
        subject_id_num = subject_id_num + subject_start_num - 2
        # Take subject score from dataframe
        subject_score = wb[wb.columns[subject_id_num]][pvs_id_num - 1]
        for question_num, question_id in enumerate(final_data['questions']):
            # Take id from questions list
            question_id_num = final_data['questions'][question_num]['id']
            # Add to final_data list of scores
            final_data['scores'].append({'id': id_num,
                                         'question_id': question_id_num,
                                         'pvs_id': pvs_id_num,
                                         'score': subject_score})
            id_num = id_num + 1

