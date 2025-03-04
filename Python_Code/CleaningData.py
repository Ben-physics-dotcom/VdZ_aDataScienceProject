import numpy as np
import pandas as pd
from tabula import read_pdf
import os


class Pdf2Json():
    def __init__(self, zoo_name: str, starting_year: int, ending_year: int, path: str):
        self.save_path = f'{path}/{zoo_name}'
        self.starting_year = starting_year
        self.ending_year = ending_year
        self.year_list = list(range(starting_year, ending_year + 1))

        # making path if not exists
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
            for year in range(starting_year, ending_year + 1):
                os.makedirs(os.path.join(self.save_path, f'{year}'))
        else:
            if not os.path.exists(self.save_path + f'/{self.starting_year}'):
                for year in range(starting_year, ending_year + 1):
                    if not os.path.exists(os.path.join(self.save_path, f'{year}')):
                        os.makedirs(os.path.join(self.save_path, f'{year}'))

    def pdf2json(self, pdf_file: str, year: int) -> None:
        df = read_pdf(pdf_file, pages='all')
        for i, d in enumerate(df):
            d.to_json(os.path.join(self.save_path, f'/{year}/table_{i}.json'))
            del d
        del df

    @staticmethod
    def pdf2json_above2down(pdf_file: str, year: int, path: str) -> None:
        df = read_pdf(pdf_file, pages='all')
        for i, d in enumerate(df):
            d.to_json(os.path.join(f'{path}/{year}/table_{i}.json'))
            del d
        del df

    def pdf2json_list(self, pdf_list: list) -> None:
        """
        Description: Convert list of pdf files to json files.

        Warning: Length of pdf_list and year_list must be equal and you need the pdf file from each year
        """
        if len(pdf_list) == len(self.year_list):
            for pdf, year in zip(pdf_list, self.year_list):
                dfs = read_pdf(pdf, pages='all')
                for i, d in enumerate(dfs):
                    if i < 10:
                        d.to_json(os.path.join(self.save_path, f'/{year}/table_00{i}.json'))
                    elif i < 100 and i >= 10:
                        d.to_json(os.path.join(self.save_path, f'/{year}/table_0{i}.json'))
                    else:
                        d.to_json(os.path.join(self.save_path, f'/{year}/table_{i}.json'))

        else:
            print('Length of pdf_list and year_list must be equal.')


class Berlin(Pdf2Json):
    def __init__(self, zoo_name: str, starting_year: int, ending_year: int, path: str):
        super().__init__(zoo_name, starting_year, ending_year, path)
        self.save_path = f'{path}/{zoo_name}'
        self.starting_year = starting_year
        self.ending_year = ending_year
        self.year_list = list(range(starting_year, ending_year + 1))
        self.name_dict = {
            0: 'Zoo',
            1: 'Aquarium',
            2: "Zoo_Aquarium",
            3: 'Tierpark'
        }
        self.tickets_types = [
            'Erwachsene', 'Erm#ßigte',
            'Kinder', 'Andere Eintrittsgelder'
        ]

        # making path if not exists
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
            for year in range(starting_year, ending_year + 1):
                os.makedirs(os.path.join(self.save_path, f'{year}'))
        else:
            for year in range(starting_year, ending_year + 1):
                if not os.path.exists(os.path.join(self.save_path, f'{year}')):
                    os.makedirs(os.path.join(self.save_path, f'{year}'))

    def correcting_files(self, year: int) -> None:
        """
        Description: Correcting the files for the year 2007 and 2008
        """
        files = [f for f in os.listdir(f'{self.save_path}/{year}') if f.endswith('.json') and f.startswith('table_')]
        for file in files:
            parts = file.split('_')
            if len(parts) != 2:
                continue

            try:
                number = int(parts[1].split('.')[0])
            except ValueError:
                continue

            new_name = f'table_{number:03d}.json'

            newpath = os.path.join(f'{self.save_path}/{year}', new_name)

            # Renaming
            os.rename(os.path.join(f'{self.save_path}/{year}', file), newpath)

    @staticmethod
    def value_replacements(df: pd.DataFrame, rows: list, col: int, col_replacements: list):
        if len(rows) == len(col_replacements):
            for i in range(len(rows)):
                df.iloc[rows[i], col] = col_replacements[i]
        else:
            print('Row list and Column replacements must have the same length.')

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
        df = df[[cols[0], 'Jahr', 'Eintrittskarten', 'Vorjahr', 'Eintrittskarten_Vorjahr', '+/- Vorjahr in %']]
        return df
