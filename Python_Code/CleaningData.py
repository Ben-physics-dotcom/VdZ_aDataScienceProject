import numpy as np
import pandas as pd
from tabula import read_pdf
import os
class Pdf2Json():
    def __init__(self, zoo_name: str):
        self.save_path = f'Data/{zoo_name}'

        # making path if not exists
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

class Berlin():
    def __init__(self, zoo_name: str):
        self.save_path = f'Data/{zoo_name}'

        # making path if not exists
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def pdf2json(self, pdf_file: str, year: int) -> None:
        df = read_pdf(pdf_file, pages='all')
        for i, d in enumerate(df):
            d.to_json(os.path.join(self.save_path, f'/{year}/table_{i}.json'))


    @staticmethod
    def str2float(df: pd.DataFrame, col: str) -> pd.DataFrame:
        df[col] = df[col].str.replace('.', '')
        df[col] = df[col].str.replace(',', '.')
        df[col] = df[col].astype(float)
        return df

    @staticmethod
    def percentage2float(df: pd.DataFrame, col: str) -> pd.DataFrame:
        df[col] = df[col].str.replace(' %', '')
        df[col] = df[col].str.replace(',', '.')
        df[col] = df[col].astype(float)
        return df

    @staticmethod
    def eintrittskarten(df: pd.DataFrame, list_cols: list, year: int, past_year: int) -> pd.DataFrame:
        for col in list_cols:
            if 'Eintrittskarten' in col:
                df = Berlin.str2float(df, col)
            elif '+/- Vorjahr in %' == col:
                df = Berlin.percentage2float(df, col)
            else:
                continue
        year1 = np.ones(len(df)) * year
        pastyear = np.ones(len(df)) * past_year
        df['Jahr'] = year1.astype(int)
        df['Vorjahr'] = pastyear.astype(int)
        df = df.rename(columns={f'Eintrittskarten {year}': 'Eintrittskarten',
                                f'Eintrittskarten {past_year}': 'Eintrittskarten_Vorjahr'})
        cols = df.columns.tolist()
        df = df[[cols[1], 'Jahr', 'Eintrittskarten', 'Vorjahr', 'Eintrittskarten_Vorjahr', '+/- Vorjahr in %']]
        return df
