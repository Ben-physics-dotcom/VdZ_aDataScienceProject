import pandas as pd
import camelot
import pymupdf


import os
import sys

data_path = '../Data/'


def read_pdf_tables(file_path: str, pages: str = 'all') -> list:
    tables = camelot.read_pdf(file_path, pages=pages, process_background=True)
    return tables


def metadata_function(file_path: str) -> dict:
    doc = pymupdf.open(file_path)
    meta = doc.metadata
    return meta


def dict_metadata_function(meta: dict, place: str, report_type: str) -> dict:
    meta_dict = {
        'Place': place,
        'Metadata': meta,
        'Report_Type': report_type
    }
    return meta_dict


def open_dict_pkl(file_path: str) -> dict:
    with open(file_path, 'rb') as f:
        results = pd.read_pickle(f)
    return results


def save_dict_pkl(results: dict, file_path: str) -> None:
    with open(file_path, 'wb') as f:
        pd.to_pickle(results, f)


def parsing_report_df(dict_input: dict) -> dict:
    pr = {}
    for year in dict_input.keys():
        year_pa = {}
        for i in range(len(dict_input[year])):
            year_pa[i] = dict_input[year][i].parsing_report
        pr[f'{year}_parsing_report'] = year_pa
    return pr


def table_to_df(dict_input: dict) -> dict:
    pr = {}
    for year in dict_input.keys():
        year_pa = {}
        for i in range(len(dict_input[year])):
            year_pa[i] = dict_input[year][i].df
        pr[year] = year_pa
    return pr
