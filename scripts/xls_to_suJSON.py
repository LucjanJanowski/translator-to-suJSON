#!/usr/bin/env python3

import pandas as pd
import json
import os

from functions import *
from _cmd_utils import parse_args, write_to_json_file


def main():
    """
    Main program
    :return: creates final json file
    """
    cli_args = parse_args()

    # Open configuration file
    with open(cli_args.config) as configuration_file:
        cf = json.load(configuration_file)

    # Open xls file with data
    # TODO: Detect whether we are reading a CSV or XLS file
    wb = pd.read_excel(
        os.path.join(os.path.dirname(cli_args.config), cf["file_name"]),
        sheet_name=cf["sheet_hdr_name"],
        header=cf["header_row_pos"],
        skipfooter=cf["footer_rows_to_skip"]
    )

    # Define result file path
    path = cf['result_file_path']

    # Define result file name
    file_name = cf['result_file_name']

    # Create list of unique src
    src_exist = 1
    if cf['src_hdr_name'] == '':
        src_exist = None
    else:
        src_num = wb[cf['src_hdr_name']].unique()

    # Create list of unique hrc
    hrc_exist = 1
    if cf['hrc_hdr_name'] == '':
        hrc_exist = None
    else:
        hrc_num = wb[cf['hrc_hdr_name']].unique()

    # Create list of unique pvs
    pvs_exist = 1
    if cf['file_hdr_name'] == '':
        pvs_exist = None
    else:
        pvs_unique = wb[cf['file_hdr_name']].unique()

    # Chceck if dataset is tidy
    if cf['is_tidy'] is True:
        is_subject_tidy = True
    else:
        is_subject_tidy = False

    final_data = json_structure(cf)

    # Create SRC list for final_data
    if src_exist is None:
        pass
    else:
        for ind, val in enumerate(src_num):
            # Add to final_data list of src
            final_data['src'].append({'id': ind + 1,
                                      'name': val})

    # Create HRC list for final_data
    if hrc_exist is None:
        pass
    else:
        for ind, val in enumerate(hrc_num):
            # Add to final_data list of hrc
            final_data['hrc'].append({'id': ind + 1,
                                      'name': val})

    # Create PVS list for final data
    if pvs_exist is None:
        pvs_unique = pvs_unique_data(wb, cf)
        for ind, val in enumerate(pvs_unique):
            for x, y in enumerate(final_data['src']):
                # Check if SRC name is connected with any PVS
                src_name = val[1]
                if src_name == final_data['src'][x]['name']:
                    for k, l in enumerate(final_data['hrc']):
                        # Check if HRC name is connected with any PVS
                        hrc_name = val[2]
                        if hrc_name == final_data['hrc'][k]['name']:
                            # Add to final_data list of PVS
                            final_data['pvs'].append({'id': ind + 1,
                                                      'src_id': final_data['src'][x]['id'],
                                                      'hrc_id': final_data['hrc'][k]['id'],
                                                      'file_name': val[0]})
    else:
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
    if is_subject_tidy is True:
        subject_tidy(wb, cf, final_data)
    else:
        subject_no_tidy(cf, final_data)

    # TRIALS
    if is_subject_tidy is True:
        trials_tidy(wb, cf, final_data)
    else:
        trials_no_tidy(final_data)

    # SCORES
    if is_subject_tidy is True:
        scores_tidy(wb, cf, final_data)
    else:
        scores_no_tidy(wb, cf, final_data)

    # Save results to JSON file
    write_to_json_file(path, file_name, final_data)


if __name__ == "__main__":
    main()
