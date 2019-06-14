#!/usr/bin/env python3

import pandas as pd
import json
import os

from _cmd_utils import parse_args, write_to_json_file


def main():
    cli_args = parse_args()

    # Open configuration file
    with open(cli_args.config) as configuration_file:
        cf = json.load(configuration_file)

    # Open xls file with data
    wb = pd.read_excel(
        os.path.join(os.path.dirname(cli_args.config), cf["file_name"]),
        sheet_name=cf["sheet_hdr_name"],
        header=cf["header_row_pos"],
        skipfooter=cf["footer_rows_to_skip"]
    )

    # Create list of unique src
    src_num = wb[cf["src_hdr_name"]].unique()

    # Create list of unique hrc
    hrc_num = wb[cf["hrc_hdr_name"]].unique()

    # Create list of unique pvs
    pvs_unique = wb[cf['file_hdr_name']].unique()

    # Define subject scores column range
    # Take column header number of first subject
    subject_start_num = cf['score_column_range']['start']

    # Take column header number of last subject
    subject_finish_num = cf['score_column_range']['stop']

    # Define result file path
    path = cf["result_file_path"]

    # Define result file name
    file_name = cf["result_file_name"]

    # DATASET_NAME
    dataset_name = cf["dataset_name"]

    # SUJSON_VERSION
    sujson_version = "1.1-in_progress"

    # CHARACTERISTICS
    characteristics = cf["characteristics"]

    # TASKS
    tasks = cf["tasks"]

    # SCALES
    scales = cf["scales"]

    # QUESTIONS
    questions = cf["questions"]

    # Define structure of final JSON file
    final_data = {
        "dataset_name": dataset_name,
        "sujson_version": sujson_version,
        "characteristics": characteristics,
        "tasks": tasks,
        "scales": scales,
        "questions": questions,
        "src": [],
        "hrc": [],
        "pvs": [],
        "subjects": [],
        "trials": [],
        "scores": [],
    }

    # Create SRC list for final_data
    # FIXME Either define this in the configuration file or detect whether any SRC column exists
    if src_exist is None:
        pass
    else:
        for ind, val in enumerate(src_num):
            # Add to final_data list of src
            final_data['src'].append({'id': ind + 1,
                                      'name': val})

    # Create HRC list for final_data
    # FIXME Either define this in the configuration file or detect whether any HRC column exists
    if hrc_exist is None:
        pass
    else:
        for ind, val in enumerate(hrc_num):
            # Add to final_data list of hrc
            final_data['hrc'].append({'id': ind + 1,
                                      'name': val})

    # Create PVS list for final data
    for ind, val in enumerate(pvs_unique):
        # Get value of row from data
        a = wb.loc[wb[cf['file_hdr_name']] == val].index[0]
        # Get name of SRC connected with PVS
        if src_exist is None:
            pass
        else:
            src_name = wb[cf['src_hdr_name']][a]
        # Get name of HRC connected with PVS
        if hrc_exist is None:
            pass
        else:
            hrc_name = wb[cf['hrc_hdr_name']][a]

        if src_exist is not None and hrc_exist is not None:
            for x, y in enumerate(final_data['src']):
                # Check if SRC name is connected with any PVS
                if src_name == final_data['src'][x]['name']:
                    for k, l in enumerate(final_data['hrc']):
                        # Check if HRC name is connected with any PVS
                        if hrc_name == final_data['hrc'][k]['name']:
                            # Add to final_data list of PVS
                            final_data['pvs'].append({'id': ind + 1,
                                                      'src_id': final_data['src'][x]['id'],
                                                      'hrc_id': final_data['hrc'][k]['id'],
                                                      'file_name': val})
        elif src_exist is not None and hrc_exist is None:
            for x, y in enumerate(final_data['src']):
                # Check if SRC name is connected with any PVS
                if src_name == final_data['src'][x]['name']:
                    # Add to final_data list of PVS
                    final_data['pvs'].append({'id': ind + 1,
                                              'src_id': final_data['src'][x]['id'],
                                              'file_name': val})
        elif src_exist is None and hrc_exist is not None:
            for k, l in enumerate(final_data['hrc']):
                # Check if HRC name is connected with any PVS
                if hrc_name == final_data['hrc'][k]['name']:
                    # Add to final_data list of PVS
                    final_data['pvs'].append({'id': ind + 1,
                                              'hrc_id': final_data['hrc'][k]['id'],
                                              'file_name': val})
        else:
            final_data['pvs'].append({'id': ind + 1,
                                      'file_name': val})

    # SUBJECTS
    for subject, val in enumerate(range(subject_start_num, subject_finish_num + 1)):
        # Add to final_data list of subjects
        final_data['subjects'].append({'id': subject + 1})

    # TRIALS
    # FIXME "score_id" field is generated shifted by 1 (for its4s subjective data)
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
                                             'score_id': id_num + 1})
                id_num = id_num + 1

    # SCORES
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

    # Save results to JSON file
    write_to_json_file(path, file_name, final_data)


if __name__ == "__main__":
    main()
