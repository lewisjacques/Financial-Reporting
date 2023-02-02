### --- Imports --- ###

from transformers import pipeline
from os import listdir
import pandas as pd
import re

### --- Logging --- ###

import logging
logging.basicConfig(level=logging.NOTSET)
log = logging.getLogger('dev')
# INFO: Just info, DEBUG: Info & Debug
log.setLevel(logging.INFO)

### --- Filename Parsing Class --- ###

class ReportingFile:
    def __init__(
        self, 
        file_name:str, 
        statements_folder:str,
        file_name_date_format:str,
        tx_schema:dict
    ):
        """
        Class to handle statements from any particular bank

        Args:
            file_name (str): Name of the bank statement file
            statements_folder (str): Location of bank statement(s)
            file_name_date_format (str): Format of the data in the file name
                (if included)
        """

        # Set class variables
        self.f_name = file_name
        self.s_folder = statements_folder
        self.f_name_date_format = file_name_date_format
        self.tx_schema = tx_schema
        
        # Parse name and file and save as class variables
        self.parse_name()
        self.parse_file()
        self.typecast_table()

    def parse_name(self) -> None:
        s_dates = re.findall(
            self.f_name_date_format["regex"], 
            self.f_name
        )
        try:
            log.debug(f" Extracting statement dates")
            self.start_date = s_dates[0][
                self.f_name_date_format["start_date_re_index"]
            ]
            self.end_date = s_dates[0][
                self.f_name_date_format["end_date_re_index"]
            ]
        except IndexError:
            log.warning(f" Dates not recognised in file name {self.f_name}")
        except TypeError:
            log.warning(f" Start/End date not given in its file name")

    def parse_file(self) -> None:
        log.debug(f" Parsing statement")
        self.statement = pd.read_csv(
            f"{self.s_folder}{self.f_name}", 
            encoding='latin-1' # Account for errored entries
        )
        log.debug(f"Statement head:\n {self.statement.head()}")

    def typecast_table(self) -> None:
        self.statement  = self.statement.astype(self.tx_schema)
        return

class StarlingFile(ReportingFile):
    FNAME_DATE_FORMAT = {
        "regex": r"StarlingStatement_(2[0-9]{3}-[0-9]{2}-[0-9]{2})_(2[0-9]{3}-[0-9]{2}-[0-9]{2})",
        "start_date_re_index": 0,
        "end_date_re_index": 1
    }
    SCHEMA = {
        "Date":                  "object",
        "Counter Party":         "object",
        "Reference":             "object",
        "Type":                  "object",
        "Amount (GBP)":          "float64",
        "Balance (GBP)":         "float64",
        "Spending Category":     "object",
        "Notes":                 "object"
    }

    def __init__(self, file_name:str, statements_folder:str):
        """
        Class to handle Starling bank statements

        Args:
            file_name (str): Name of the bank statement file
            statements_folder (str): Location of bank statement(s)
        """

        super().__init__(
            file_name=file_name, 
            statements_folder=statements_folder,
            file_name_date_format=self.FNAME_DATE_FORMAT,
            tx_schema=self.SCHEMA
        )

class NatwestFile(ReportingFile):
    # Only has a download date
    FNAME_DATE_FORMAT = {
        "regex": r"[A-Z]*[0-9]{4}-([0-9]{8}).*",
        "start_date_re_index": None,
        "end_date_re_index": None
    }
    SCHEMA = {

    }

    def __init__(self, file_name:str, statements_folder:str):
        """
        Class to handle Natwest bank statements

        Args:
            file_name (str): Name of the bank statement file
            statements_folder (str): Location of bank statement(s)
        """

        super().__init__(
            file_name=file_name, 
            statements_folder=statements_folder,
            file_name_date_format=self.FNAME_DATE_FORMAT,
            tx_schema=self.SCHEMA
        )

class TxTableGenerator:
    BANK_NAMES = (
        "starling", "natwest"
    )

    def __init__(self, bank_name:str, statements_folder:str):
        """
        Class to generate one collated statement containing all statements
        within the statements_folder, with columns type cast and normalised
        into a consistent schema across all banks

        Args:
            bank_name (str): Name of the bank, must be a member of BANK_NAMES
            statements_folder (str): Folder containing all bank statements
        """

        assert bank_name in self.BANK_NAMES, f"Unrecognised bank, {bank_name}"
        file_names = listdir(statements_folder)
        self.all_statements = []

        if bank_name == "starling":
            for f_name in file_names: #move this inside other class
                sf = StarlingFile(f_name, statements_folder)
                self.all_statements.append(sf)
        elif bank_name == "natwest":
            for f_name in file_names: #move this inside other class
                sf = NatwestFile(f_name, statements_folder)
                self.all_statements.append(sf)
        else:
            return


statements_folder = "Statements/Natwest/"
ttg = TxTableGenerator(
    bank_name="natwest",
    statements_folder=statements_folder
)













# https://huggingface.co/spaces/joeddav/zero-shot-demo
classifier = pipeline("zero-shot-classification")

# Need a known dictionary to add predictions too if they don't already exist

sequence = "TESCO STORES-2813 LEAMINGTON SP GBR"
candidate_labels = ['INCOME', 'GROCERIES', 'SHOPPING', 'EATING_OUT']

classifier(sequence, candidate_labels)