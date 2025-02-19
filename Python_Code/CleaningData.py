import pandas as pd
import os
import numpy as np


class CleaningData():
    """
    Description:

    """
    def __init__(self, place: str, year: int) -> None:
        if not os.path.exists(f'../../Data/{place}/{year}/'):
            os.makedirs(f'../../Data/{place}/{year}/')
        self.data_path = f'../../Data/{place}/{year}/'
        self.year = year
        self.place = place
        self.list_of_files = ['passiva', 'activa', 'AcquisitionAndManufacturingCosts', 'Daytickets_Aquarium',
                              'Daytickets_Zoo', 'DepreciationBookValues', 'FeedQuantitiesConsumed', 'OtherTickets',
                              'ProfitsAndLosses', 'ZooCard_Aquarium', 'ZooCard_Zoo',
                              'StatementOfEquity', 'Liabilities', 'SalesRevenue', 'PersonnelKeyFigures',
                              'Mammals', 'Birds'
                              ]
        # DataFrames / possible SQL tables
        self.passiva = pd.DataFrame
        self.activa = pd.DataFrame
        self.AcquisitionAndManufacturingCost = pd.DataFrame
        self.DayTicketsAquarium = pd.DataFrame
        self.DayTicketsZoo = pd.DataFrame
        self.DepreciateionBookValues = pd.DataFrame
        self.FeedQuantitiesConsumed = pd.DataFrame
        self.OtherTickets = pd.DataFrame
        self.ProfitsandLosses = pd.DataFrame
        self.ZooCardAquarium = pd.DataFrame
        self.ZooCardZoo = pd.DataFrame
        self.StatementOfEquity = pd.DataFrame
        self.Liabilities = pd.DataFrame
        self.SalesRevenue = pd.DataFrame
        self.PersonnelKeyFigures = pd.DataFrame
        self.Mammals = pd.DataFrame
        self.Birds = pd.DataFrame

    @staticmethod
    def check_if_path_file_not_exist_and_create_it(path_file: str) -> None:
        if not os.path.exists(path_file):
            os.makedirs(path_file)

    def creating_empty_csv(self) -> None:
        path = self.data_path
        CleaningData.check_if_path_file_not_exist_and_create_it(path)
        for file in self.list_of_files:
            x = path + file + '.csv'
            CleaningData.check_if_path_file_not_exist_and_create_it(x)

    def read_csv(self, file_name: str, sep=';') -> pd.DataFrame:
        df = pd.read_csv(
            filepath_or_buffer=self.data_path + file_name,
            sep=sep
        )
        return df

    def write_csv(self, df: pd.DataFrame, file_name: str) -> None:
        df.to_csv(
            path_or_buf=self.data_path + file_name,
            sep=','
        )

    def read_all_csv_files(self, sep=';') -> None:
        self.passiva = self.read_csv('passiva.csv', sep)
        self.activa = self.read_csv('activa.csv', sep)
        self.AcquisitionAndManufacturingCost = self.read_csv('AcquisitionAndManufacturingCosts.csv', sep)
        self.DayTicketsAquarium = self.read_csv('Daytickets_Aquarium.csv', sep)
        self.DayTicketsZoo = self.read_csv('Daytickets_Zoo.csv', sep)
        self.DepreciationBookValues = self.read_csv('DepreciationBookValues.csv', sep)
        self.FeedQuantitiesConsumed = self.read_csv('FeedQuantitiesConsumed.csv', sep)
        self.ProfitsandLosses = self.read_csv('ProfitsAndLosses.csv', sep)
        self.ZooCardAquarium = self.read_csv('ZooCard_Aquarium.csv', sep)
        self.ZooCardZoo = self.read_csv('ZooCard_Zoo.csv', sep)
        self.OtherTickets = self.read_csv('OtherTickets.csv', sep)

    # Cleaning Passiva/Activa Berlin
    def cleaning_act_pass(self) -> None:
        """
        Description: Cleaning the data in the passiva and activa tables
        """
        self.passiva = self.passiva.dropna()
        self.activa = self.activa.dropna()

        for i in range(len(self.activa.columns) - 1):
            i += 1
            for j in range(len(self.activa)):
                if self.activa.iloc[j, i] == 'in EUR':
                    self.activa.iloc[j, i] = np.nan
            self.activa[self.activa.columns[i]] = self.activa[self.activa.columns[i]].astype(float)
            self.activa[self.passiva.columns[i]] = self.activa[self.passiva.columns[i]].astype(float)

    # points, commas, int and float values
    @staticmethod
    def change_cols_in_numerical_data(df: pd.DataFrame, column: str, intfloat=0):
        df[column] = df[column].str.replace('.', '')
        df[column] = df[column].str.replace(',', '.')
        if intfloat == 0:
            df[column] = df[column].astype(int)
        else:
            df[column] = df[column].astype(float)
        return df

    # Grouping data tables in dictionaries
    def development_of_fixed_assets(self) -> dict:
        dictionary = {
            'Aquisition costs': self.AcquisitionAndManufacturingCost,
            'Depreciation and book values': self.DepreciationBookValues
        }
        return dictionary

    def cards_dictionary(self) -> dict:
        dictionary = {
            'Daytickets Zoo': self.DayTicketsZoo,
            'Daytickets Aquarium': self.DayTicketsAquarium,
            'ZooCard Zoo': self.ZooCardZoo,
            'ZooCard Aquarium': self.ZooCardAquarium,
            'Other Tickets': self.OtherTickets
        }
        return dictionary

    def animals(self) -> dict:
        dictionary = {
            'Mammals': self.Mammals,
            'Birds': self.Birds
        }
        return dictionary
