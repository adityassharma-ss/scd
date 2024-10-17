import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font
from openpyxl import Workbook
import re

class IOHandler:
    @staticmethod
    def load_csv(file_paths):
        """Loads cloud control data from multiple dataset files."""
        dataframes = []
        for file_path in file_paths:
            try:
                # Try UTF-8 first
                df = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                try:
                    # If UTF-8 fails, try 'latin-1'
                    df = pd.read_csv(file_path, encoding='latin-1')
                except Exception as e:
                    print(f"Error reading file {file_path}: {str(e)}")
                    continue
            dataframes.append(df)

        # Combine all datasets into one
        if dataframes:
            return pd.concat(dataframes, ignore_index=True)
        return None

    # Rest of the class remains the same...
