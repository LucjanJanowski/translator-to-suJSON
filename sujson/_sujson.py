import json
import pandas as pd
import numpy as np
import pickle
import os
import csv
import pprint

from . import __version__
from ._errors import SujsonError
from ._logger import setup_custom_logger

logger = setup_custom_logger("sujson")


class Sujson:
    def __init__(self, force=False, dry_run=False):
        """Initialize suJSON

        Keyword Arguments:
            force {bool} -- force overwriting output files (default: {False})
            dry_run {bool} -- only run in dry, do not do anything (default: {False})
        """
        self.force = force
        self.dry_run = dry_run

        # internal data, default config
        self.config = {
            "sheet_hdr_name": 0,
            "header": 0,
            "skipfooter": 0
        }

        # default suJSON data
        self.sujson = {
            "src": [],
            "hrc": [],
            "pvs": [],
            "subjects": [],
            "trials": [],
            "scores": [],
        }

        self.dataframe = {
            "stimulus_id": [],
            "trial_id": [],
            "subject_id": [],
            "scores": [],
            "timestamp": [],
            "session_num": [],
            "order_num": [],
            "subject": [],
            "src": [],
            "hrc": [],
        }

    def _write_data_to_json(self, output_file):
        # resolve numpy type problem
        def default_converter(o):
            if isinstance(o, np.int64):
                return int(o)

        if output_file:
            if not self.dry_run:
                # TODO Consider catching the "file does not exist" exception and rising the suJSON exception
                with open(output_file, "w") as out_f:
                    logger.info("Writing suJSON data to {}".format(output_file))
                    json.dump(self.sujson, out_f, indent=4, default=default_converter)
            else:
                logger.info("Would write suJSON data to {}".format(output_file))
        else:
            if not self.dry_run:
                print(json.dumps(self.sujson, indent=4, default=default_converter))
            else:
                logger.info("Would print suJSON data to STDOUT")

    def _json_structure(self):
        # DATASET_NAME
        dataset_name = self.config['dataset_name']

        # SUJSON_VERSION
        sujson_version = __version__

        # CHARACTERISTICS
        characteristics = self.config['characteristics']

        # TASKS
        tasks = self.config['tasks']

        # SCALES
        scales = self.config['scales']

        # QUESTIONS
        questions = self.config['questions']

        # Define structure of final JSON file
        self.sujson = {'dataset_name': dataset_name,
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
        return self.sujson

    def _pvs_id_list(self, wb, pvs_unique):
        pvs_list = []
        pvs_list_id = []
        for helper_ind, row in wb.iterrows():
            for ind, val in enumerate(pvs_unique):
                if row[self.config['src_hdr_name']] == val[1] and row[self.config['hrc_hdr_name']] == val[2]:
                    pvs_list.append(val[0])
        for helper_ind, id in enumerate(pvs_list):
            for ind, val in enumerate(self.sujson['pvs']):
                if val['file_name'] == id:
                    pvs_list_id.append(val['id'])
        return pvs_list_id

    def _subject_tidy(self, wb):
        subjects = wb[self.config['subject_hdr_name']].unique()
        for subject, val in enumerate(subjects):
            # Add to final_data list of src
            self.sujson['subjects'].append({'id': subject + 1,
                                            'name': val})

    def _subject_no_tidy(self):
        # Define subject scores column range
        # Take column header number of first subject
        subject_start_num = self.config['score_column_range']['start']

        # Take column header number of last subject
        subject_finish_num = self.config['score_column_range']['stop']

        for subject, val in enumerate(range(subject_start_num, subject_finish_num + 1)):
            # Add to final_data list of subjects
            self.sujson['subjects'].append({'id': subject + 1})

    def _pvs_unique_data(self, wb):
        pvs_unique = []
        used_name = []
        for helper_ind, row in wb.iterrows():
            if row[self.config['src_hdr_name']] + "_" + row[self.config['hrc_hdr_name']] not in used_name:
                pvs_unique.append((row[self.config['src_hdr_name']] + "_" + row[self.config['hrc_hdr_name']],
                                   row[self.config['src_hdr_name']],
                                   row[self.config['hrc_hdr_name']]))
                used_name.append(row[self.config['src_hdr_name']] + "_" + row[self.config['hrc_hdr_name']])
        return pvs_unique

    def _trials_tidy(self, wb):
        id_num = 1
        pvs_unique = self._pvs_unique_data(wb)
        for task_num, task_id in enumerate(self.sujson['tasks']):
            # Take id from tasks list
            task_id_num = self.sujson['tasks'][task_num]['id']
            subjects = wb[self.config['subject_hdr_name']]
            subjects_unique = wb[self.config['subject_hdr_name']].unique()
            pvs_list = self._pvs_id_list(wb, pvs_unique)
            for id, val in enumerate(subjects):
                for subject_id_num, subject_id in enumerate(subjects_unique):
                    if val == subject_id:
                        self.sujson['trials'].append({'id': id_num,
                                                      'subject_id': subject_id_num + 1,
                                                      'task_id': task_id_num,
                                                      'pvs_id': pvs_list[id_num - 1],
                                                      'score_id': id_num})
                        id_num = id_num + 1

    def _trials_no_tidy(self):
        id_num = 1
        for subject_num, subject_id in enumerate(self.sujson['subjects']):
            # Take id from subjects list
            subject_id_num = self.sujson['subjects'][subject_num]['id']
            for task_num, task_id in enumerate(self.sujson['tasks']):
                # Take id from tasks list
                task_id_num = self.sujson['tasks'][task_num]['id']
                for pvs_num, pvs_id in enumerate(self.sujson['pvs']):
                    # Take id from pvs list
                    pvs_id_num = self.sujson['pvs'][pvs_num]['id']
                    # Add to final_data list of trials
                    self.sujson['trials'].append({'id': id_num,
                                                  'subject_id': subject_id_num,
                                                  'task_id': task_id_num,
                                                  'pvs_id': pvs_id_num,
                                                  'score_id': id_num})
                    id_num = id_num + 1

    def _scores_tidy(self, wb):
        id_num = 1
        for score_num, score_id in enumerate(self.sujson['trials']):
            # Take pvs_id from trials list
            pvs_id_num = self.sujson['trials'][score_num]['pvs_id']
            # Take subject score from dataframe
            subject_score = wb[self.config['score_column']][id_num - 1]
            for question_num, question_id in enumerate(self.sujson['questions']):
                # Take id from questions list
                question_id_num = self.sujson['questions'][question_num]['id']
                # Add to final_data list of scores
                self.sujson['scores'].append({'id': id_num,
                                              'question_id': question_id_num,
                                              'pvs_id': pvs_id_num,
                                              'score': subject_score})
                id_num = id_num + 1

    def _scores_no_tidy(self, wb):
        # Take column header number of first subject
        subject_start_num = self.config['score_column_range']['start']

        # Scores
        id_num = 1
        for score_num, score_id in enumerate(self.sujson['trials']):
            # Take pvs_id from trials list
            pvs_id_num = self.sujson['trials'][score_num]['pvs_id']
            # Take subject_id from trials list
            subject_id_num = self.sujson['trials'][score_num]['subject_id']
            subject_id_num = subject_id_num + subject_start_num - 2
            # Take subject score from dataframe
            subject_score = wb[wb.columns[subject_id_num]][pvs_id_num - 1]
            for question_num, question_id in enumerate(self.sujson['questions']):
                # Take id from questions list
                question_id_num = self.sujson['questions'][question_num]['id']
                # Add to final_data list of scores
                self.sujson['scores'].append({'id': id_num,
                                              'question_id': question_id_num,
                                              'pvs_id': pvs_id_num,
                                              'score': subject_score})
                id_num = id_num + 1

    def _read_sujson(self, input_file):
        logger.info("Reading suJSON from {}".format(input_file))
        with open(input_file) as in_f:
            self.sujson = json.load(in_f)

    def _read_config(self, config_file):
        if config_file is not None:
            logger.info("Reading config from {}".format(config_file))
            with open(config_file) as cf:
                # TODO validate config!
                self.config = json.load(cf)
        else:
            logger.warning("No config file given. We have to make many assumptions...")

    def import_xslx(self, input_file, config_file, output_file=None):
        # TODO @Qub3k Simplify this function (probably by splitting it into multiple smaller functions)
        if output_file is not None:
            output_suffix = os.path.splitext(output_file)[1]
            if output_suffix not in [".json"]:
                raise SujsonError("Unsupported output file suffix {}".format(output_suffix))

        self._read_config(config_file)

        logger.info("Reading data from {}".format(input_file))
        wb = pd.read_excel(
            input_file,
            sheet_name=self.config["sheet_hdr_name"],
            header=self.config["header_row_pos"],
            skipfooter=self.config["footer_rows_to_skip"],
        )

        # TODO @matix7290 Implement here the heuristics to detect whether we are dealing with tidy or non-tidy data.
        #  Start from checking the number of rows in the wb DataFrame.

        # Create list of unique src

        self.sujson = self._json_structure()

        src_exist = 1
        if self.config['src_hdr_name'] == '':
            src_exist = None
        else:
            src_num = wb[self.config['src_hdr_name']].unique()

        # Create list of unique hrc
        hrc_exist = 1
        if self.config['hrc_hdr_name'] == '':
            hrc_exist = None
        else:
            hrc_num = wb[self.config['hrc_hdr_name']].unique()

        # Create list of unique pvs
        pvs_exist = 1
        if self.config['file_hdr_name'] == '':
            pvs_exist = None
        else:
            pvs_unique = wb[self.config['file_hdr_name']].unique()

        # Chceck if dataset is tidy
        if self.config['is_tidy'] is True:
            is_subject_tidy = True
        else:
            is_subject_tidy = False

        # Create SRC list for final_data
        if src_exist is None:
            pass
        else:
            for ind, val in enumerate(src_num):
                # Add to final_data list of src
                self.sujson['src'].append({'id': ind + 1,
                                           'name': val})

        # Create HRC list for final_data
        if hrc_exist is None:
            pass
        else:
            for ind, val in enumerate(hrc_num):
                # Add to final_data list of hrc
                self.sujson['hrc'].append({'id': ind + 1,
                                           'name': val})

        # Create PVS list for final data
        if pvs_exist is None:
            pvs_unique = self._pvs_unique_data(wb)
            for ind, val in enumerate(pvs_unique):
                for x, y in enumerate(self.sujson['src']):
                    # Check if SRC name is connected with any PVS
                    src_name = val[1]
                    if src_name == self.sujson['src'][x]['name']:
                        for k, l in enumerate(self.sujson['hrc']):
                            # Check if HRC name is connected with any PVS
                            hrc_name = val[2]
                            if hrc_name == self.sujson['hrc'][k]['name']:
                                # Add to final_data list of PVS
                                self.sujson['pvs'].append({'id': ind + 1,
                                                           'src_id': self.sujson['src'][x]['id'],
                                                           'hrc_id': self.sujson['hrc'][k]['id'],
                                                           'file_name': val[0]})
        else:
            for ind, val in enumerate(pvs_unique):
                # Get value of row from data
                a = wb.loc[wb[self.config['file_hdr_name']] == val].index[0]
                # Get name of SRC connected with PVS
                if src_exist is None:
                    pass
                else:
                    src_name = wb[self.config['src_hdr_name']][a]
                # Get name of HRC connected with PVS
                if hrc_exist is None:
                    pass
                else:
                    hrc_name = wb[self.config['hrc_hdr_name']][a]

                if src_exist is not None and hrc_exist is not None:
                    for x, y in enumerate(self.sujson['src']):
                        # Check if SRC name is connected with any PVS
                        if src_name == self.sujson['src'][x]['name']:
                            for k, l in enumerate(self.sujson['hrc']):
                                # Check if HRC name is connected with any PVS
                                if hrc_name == self.sujson['hrc'][k]['name']:
                                    # Add to final_data list of PVS
                                    self.sujson['pvs'].append({'id': ind + 1,
                                                               'src_id': self.sujson['src'][x]['id'],
                                                               'hrc_id': self.sujson['hrc'][k]['id'],
                                                               'file_name': val})
                elif src_exist is not None and hrc_exist is None:
                    for x, y in enumerate(self.sujson['src']):
                        # Check if SRC name is connected with any PVS
                        if src_name == self.sujson['src'][x]['name']:
                            # Add to final_data list of PVS
                            self.sujson['pvs'].append({'id': ind + 1,
                                                       'src_id': self.sujson['src'][x]['id'],
                                                       'file_name': val})
                elif src_exist is None and hrc_exist is not None:
                    for k, l in enumerate(self.sujson['hrc']):
                        # Check if HRC name is connected with any PVS
                        if hrc_name == self.sujson['hrc'][k]['name']:
                            # Add to final_data list of PVS
                            self.sujson['pvs'].append({'id': ind + 1,
                                                       'hrc_id': self.sujson['hrc'][k]['id'],
                                                       'file_name': val})
                else:
                    self.sujson['pvs'].append({'id': ind + 1,
                                               'file_name': val})

        # SUBJECTS
        if is_subject_tidy is True:
            self._subject_tidy(wb)
        else:
            self._subject_no_tidy()

        # TRIALS
        if is_subject_tidy is True:
            self._trials_tidy(wb)
        else:
            self._trials_no_tidy()

        # SCORES
        if is_subject_tidy is True:
            self._scores_tidy(wb)
        else:
            self._scores_no_tidy(wb)

        # Save results to JSON file
        self._write_data_to_json(output_file)

    def import_csv(self, input_file, config_file, output_file=None):
        """
        Function takes subjective test data from input_file of .csv format and converts it to suJSON format
        using config_file. Output data is written to output_file (.json)
        or to STDOUT when no output file specified.

        :param input_file: .csv file with data from subjective test
        :param config_file: configuration file for input_file
        :param output_file: output file to which suJSON will be written
        """

        # TODO (future) Use the heuristics detecting whether we are dealing with a tidy input

        input_suffix = os.path.splitext(input_file)[1]
        if input_suffix not in [".csv"]:
            raise SujsonError("Unsupported input file suffix {}".format(input_suffix))

        if output_file is not None:
            output_suffix = os.path.splitext(output_file)[1]
            if output_suffix not in [".json"]:
                raise SujsonError("Unsupported output file suffix {}".format(output_suffix))

        self._read_config(config_file)

        try:
            infile = pd.read_csv(input_file)
        except FileNotFoundError:
            raise SujsonError("That is not a correct input path: {}".format(input_file))

        infile = infile.loc[infile[self.config['experiment_column']] == self.config['experiment_number']]

        self.sujson = self._json_structure()

        # filling hrc field in sujson
        hrc_id = 1
        for hrc_name in infile.get(self.config['hrc_hdr_name']).unique():
            self.sujson.get('hrc').append({'id': hrc_id, 'name': hrc_name})
            hrc_id = hrc_id+1

        # filling src field in sujson
        src_id = 1
        for src_name in infile.get(self.config['src_hdr_name']).unique():
            self.sujson.get('src').append({'id': src_id, 'name': src_name})
            src_id = src_id + 1

        # filling pvs field in sujson
        unique_pvs_list = []
        for index, row in infile.iterrows():
            if row.get(self.config['file_hdr_name']) not in unique_pvs_list:
                unique_pvs_list.append(row.get(self.config['file_hdr_name']))
                src_index = self.find_by_value('name', row.get(self.config['src_hdr_name']), self.sujson.get('src'))
                hrc_index = self.find_by_value('name', row.get(self.config['hrc_hdr_name']), self.sujson.get('hrc'))
                self.sujson.get('pvs').append(
                    {
                        'id': row.get(self.config['pvs_hdr_name']),
                        'src_id': self.sujson.get('src')[src_index].get('id'),
                        'hrc_id': self.sujson.get('hrc')[hrc_index].get('id'),
                        'name': row.get(self.config['file_hdr_name'])
                    }
                )

        # filling subjects field in sujson
        subject_id = 1
        for subject in infile.get(self.config['subject_column_name']).unique():
            self.sujson.get('subjects').append({'id': subject_id, 'name': subject})
            subject_id = subject_id+1

        # filling trials and socres fields in sujson
        score_id = 1
        trial_id = 1
        for index, row in infile.iterrows():
            self.sujson.get('trials').append(
                {'id': trial_id,
                 'subject_id': row.get(self.config['subject_column_name']),
                 'task_id': 1,
                 'pvs_id': row.get(self.config['src_hdr_name']),
                 'score_id': score_id}
            )
            self.sujson.get('scores').append({'id': score_id, 'score': row.get(self.config['score_column'])})
            score_id = score_id+1
            trial_id = trial_id+1

        self._write_data_to_json(output_file)

    def raw_export(self, outfile):
        """
        Function saves suJSON data to pickle

        :param outfile: output file to save data in it
        """
        pickle.dump(self.sujson, outfile)

    def find_by_value(self, dict_key, dict_value, searched_list):
        """
        Function takes list of dictionaries (searched_list) and finds which dictionary has assigned dict_value to
        dict_key in it. It returns index of the first dictionary in list that has dict_value assigned to dict_key.
        If there is no dict_value in any dictionary, None is returned.

        :param dict_key: name of the key we are interested in
        :param dict_value: value of dict_key we want to find
        :param searched_list: list of dictionaries
        :return: index of the first dictionary in list that has dict_value assigned to dict_key or None if there is no such value
        """
        index = 0
        for i in searched_list:
            if i.get(dict_key) == dict_value:
                return index
            index = index + 1
        return None

    def build_dataframe(self, trial, pvs_id, score_id):
        """
        Function fills self.dataframe dictionary with values from suJSON. Resulting dictionary has following
        keys: stimulus_id, scores, trial_id, subject_id, timestamp, session_num,
        subject, src and hrc.

        :param trial: single element form self.sujson['trials']
        :param pvs_id: single pvs_id value from trial element
        :param score_id: single score_id value from trial element
        """
        self.dataframe['stimulus_id'].append(pvs_id)
        self.dataframe['scores'].append(self.sujson['scores'][self.find_by_value('id', score_id, self.sujson['scores'])]
                                        ['score'])
        self.dataframe['trial_id'].append(trial['id'])
        self.dataframe['subject_id'].append(trial['subject_id'])
        self.dataframe['timestamp'].append(self.sujson['scores']
                                           [self.find_by_value('id', score_id, self.sujson['scores'])].get('timestamp'))
        self.dataframe['session_num'].append(trial.get('session_num'))
        self.dataframe['order_num'].append(trial.get('order_num'))

        self.dataframe['subject'].append(self.sujson['subjects']
                                         [self.find_by_value('id', trial['subject_id'], self.sujson['subjects'])]
                                         .get('characteristics'))

        src_id = self.sujson['pvs'][self.find_by_value('id', pvs_id, self.sujson['pvs'])].get('src_id')
        hrc_id = self.sujson['pvs'][self.find_by_value('id', pvs_id, self.sujson['pvs'])].get('hrc_id')

        if src_id is not None:
            self.dataframe['src'].append(self.sujson['src'][self.find_by_value('id', src_id, self.sujson['src'])]
                                         .get('name'))
        else:
            self.dataframe['src'].append(None)

        if hrc_id is not None:
            self.dataframe['hrc'].append(self.sujson['hrc'][self.find_by_value('id', hrc_id, self.sujson['hrc'])]
                                         .get('characteristics'))
        else:
            self.dataframe['hrc'].append(None)

    def pandas_export(self):
        """
        Function iterates over self.sujson['trials'] and calls build_dataframe() function
        for each trial, then creates Pandas DataFrame.

        :return: scores_data_frame: Pandas DataFrame resulted from self.sujson
        """
        # Iterate over all trials
        for trial in self.sujson['trials']:
            # TODO (optional) @awro1444 What if the same person scores the same stimulus two or more times? Please note
            #  that in this situation you will have only one value under the "pvs_id" key, but a list of values under
            #  the "score_id" key.
            if type(trial['pvs_id']) is list and type(trial['score_id']) is list:
                assert len(trial['pvs_id']) == len(trial['score_id'])
                # TODO (optional) @awro1444 What if in a single trial one person scores two stimuli at once? In other
                #  words, what if one score is associated with two stimuli?
                for pvs_id, score_id in zip(trial['pvs_id'], trial['score_id']):

                    self.build_dataframe(trial, pvs_id, score_id)

            else:
                self.build_dataframe(trial, trial['pvs_id'], trial['score_id'])

                # # FIXME Fix the problem with suJSONs that do not have the "src_id" key

        scores_data_frame = pd.DataFrame({'stimulus_id': self.dataframe['stimulus_id'],
                                          'subject_id': self.dataframe['subject_id'],
                                          'trial_id': self.dataframe['trial_id'],
                                          'score': self.dataframe['scores'],
                                          'timestamp': self.dataframe['timestamp'],
                                          'session_num': self.dataframe['session_num'],
                                          'order_num': self.dataframe['order_num'],
                                          'src': self.dataframe['src']})

        for characteristic in self.dataframe['hrc']:
            if characteristic is not None:
                for value in characteristic:
                    scores_data_frame['hrc: ' + value] = characteristic.get(value)
            else:
                scores_data_frame['hrc'] = None

        for characteristic in self.dataframe['subject']:
            if characteristic is not None:
                for value in characteristic:
                    scores_data_frame['subject: ' + value] = characteristic.get(value)
            else:
                scores_data_frame['subject'] = None

        return scores_data_frame

    def export(self, input_file, output_format, output_file):
        """
        Function takes from input_file data of suJSON format and saves it to output_file.
        If output_format is "suJSON" it writes it as raw suJSON.
        If output_format is "Pandas" it translates it into Pandas DataFrame.

        :param input_file: path to file with data saved in suJSON format
        :param output_format: format of output, possible values: "suJSON" or "Pandas"
        :param output_file: path to output file that we want output data to be saved as
        :return: status - True if successful
        """

        suffix = os.path.splitext(input_file)[1]
        if suffix not in [".json"]:
            raise SujsonError("Unsupported input file suffix {}".format(suffix))

        output_suffix = os.path.splitext(output_file)[1]
        if output_suffix not in [".pickle", ".csv"]:
            raise SujsonError("Unsupported output file suffix {}".format(output_suffix))

        if output_format not in ["suJSON", "Pandas"]:
            raise SujsonError("Unsupported format argument {} - possible 'suJSON' or 'Pandas'".format(output_format))

        if output_format == "suJSON" and output_suffix == ".csv":
            raise SujsonError("For suJSON format only .pickle output file is allowed")

        try:
            self._read_sujson(input_file)
        except FileNotFoundError as e:
            raise SujsonError("That is not a correct input path: {}".format(input_file)) from e

        try:
            outfile = open(output_file, 'wb')
        except FileNotFoundError as e:
            raise SujsonError("That is not a correct output path: {}".format(output_file)) from e

        if output_format == "suJSON":
            # exporting suJSON dictionary to pickle
            self.raw_export(outfile)

        if output_format == "Pandas":
            # exporting to pickle as Pandas Data Frame
            df = self.pandas_export()
            if os.path.splitext(output_file)[1] in [".csv"]:
                df.to_csv(output_file)
            else:
                pickle.dump(df, outfile)

        outfile.close()

        return True  # "suJSON file successfully exported to a pickle"
