import json
import pandas as pd
import numpy as np

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

    def _write_data_to_json(self, output_file):
        # resolve numpy type problem
        def default_converter(o):
            if isinstance(o, np.int64):
                return int(o)

        if output_file:
            if not self.dry_run:
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

    def import_xslx(self, input_file, output_file=None, config_file=None):
        self._read_config(config_file)

        logger.info("Reading data from {}".format(input_file))
        wb = pd.read_excel(
            input_file,
            sheet_name=self.config["sheet_hdr_name"],
            header=self.config["header_row_pos"],
            skipfooter=self.config["footer_rows_to_skip"],
        )

        # Create list of unique src
        src_num = wb[self.config["src_hdr_name"]].unique()

        # Create list of unique hrc
        hrc_num = wb[self.config["hrc_hdr_name"]].unique()

        # Create list of unique pvs
        pvs_unique = wb[self.config["file_hdr_name"]].unique()

        # Define subject scores column range
        # Take column header number of first subject
        subject_start_num = self.config["score_column_range"]["start"]

        # Take column header number of last subject
        subject_finish_num = self.config["score_column_range"]["stop"]

        # DATASET_NAME
        dataset_name = self.config["dataset_name"]

        # SUJSON_VERSION
        sujson_version = __version__

        # CHARACTERISTICS
        characteristics = self.config["characteristics"]

        # TASKS
        tasks = self.config["tasks"]

        # SCALES
        scales = self.config["scales"]

        # QUESTIONS
        questions = self.config["questions"]

        # Define structure of final JSON file
        self.sujson = {
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

        # Create SRC list for self.sujson
        for ind, val in enumerate(src_num):
            # Add to self.sujson list of src
            self.sujson["src"].append({"id": ind + 1, "name": val})

        # Create HRC list for self.sujson
        for ind, val in enumerate(hrc_num):
            # Add to self.sujson list of hrc
            self.sujson["hrc"].append({"id": ind + 1, "name": val})

        # Create PVS list for final data
        for ind, val in enumerate(pvs_unique):
            # Get value of row from data
            a = wb.loc[wb[self.config["file_hdr_name"]] == val].index[0]
            # Get name of SRC connected with PVS
            src_name = wb[self.config["src_hdr_name"]][a]
            # Get name of HRC connected with PVS
            hrc_name = wb[self.config["hrc_hdr_name"]][a]
            for x, y in enumerate(self.sujson["src"]):
                # Check if SRC name is connected with any PVS
                if src_name == self.sujson["src"][x]["name"]:
                    for k, l in enumerate(self.sujson["hrc"]):
                        # Check if HRC name is connected with any PVS
                        if hrc_name == self.sujson["hrc"][k]["name"]:
                            # Add to self.sujson list of PVS
                            self.sujson["pvs"].append(
                                {
                                    "id": ind + 1,
                                    "src_id": self.sujson["src"][x]["id"],
                                    "hrc_id": self.sujson["hrc"][k]["id"],
                                    "file_name": val,
                                }
                            )

        # SUBJECTS
        for subject, val in enumerate(range(subject_start_num, subject_finish_num + 1)):
            # Add to self.sujson list of subjects
            self.sujson["subjects"].append({"id": subject + 1})

        # TRIALS
        id_num = 1
        for subject_num, subject_id in enumerate(self.sujson["subjects"]):
            # Take id from subjects list
            subject_id_num = self.sujson["subjects"][subject_num]["id"]
            for task_num, task_id in enumerate(self.sujson["tasks"]):
                # Take id from tasks list
                task_id_num = self.sujson["tasks"][task_num]["id"]
                for pvs_num, pvs_id in enumerate(self.sujson["pvs"]):
                    # Take id from pvs list
                    pvs_id_num = self.sujson["pvs"][pvs_num]["id"]
                    # Add to self.sujson list of trials
                    self.sujson["trials"].append(
                        {
                            "id": id_num,
                            "subject_id": subject_id_num,
                            "task_id": task_id_num,
                            "pvs_id": pvs_id_num,
                            "score_id": id_num,
                        }
                    )
                    id_num = id_num + 1

        # SCORES
        id_num = 1
        for score_num, score_id in enumerate(self.sujson["trials"]):
            # Take pvs_id from trials list
            pvs_id_num = self.sujson["trials"][score_num]["pvs_id"]
            # Take subject_id from trials list
            subject_id_num = self.sujson["trials"][score_num]["subject_id"]
            subject_id_num = subject_id_num + subject_start_num - 2
            # Take subject score from dataframe
            subject_score = wb[wb.columns[subject_id_num]][pvs_id_num - 1]
            for question_num, question_id in enumerate(self.sujson["questions"]):
                # Take id from questions list
                question_id_num = self.sujson["questions"][question_num]["id"]
                # Add to self.sujson list of scores
                self.sujson["scores"].append(
                    {
                        "id": id_num,
                        "question_id": question_id_num,
                        "pvs_id": pvs_id_num,
                        "score": subject_score,
                    }
                )
                id_num = id_num + 1

        # Save results to JSON file
        self._write_data_to_json(output_file)

    def import_csv(self, input_file, output_file=None, config_file=None):
        self._read_config(config_file)
        raise SujsonError("import_csv is not implemented yet!")
        # TODO import CSV file

    def export(self, input_file, output_file=None):
        self._read_sujson(input_file)
        raise SujsonError("export is not implemented yet!")
        # TODO export suJSON file
