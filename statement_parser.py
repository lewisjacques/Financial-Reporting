### --- Imports --- ###

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
        file_name, 
        statements_folder,
        file_name_date_format
    ):
        # Set class variables
        self.f_name = file_name
        self.s_folder = statements_folder
        self.f_name_date_format = file_name_date_format
        
        # Parse name and file and save as class variables
        self.parse_name()
        self.parse_file()

    def parse_name(self) -> None:
        s_dates = re.findall(self.f_name_date_format, self.f_name)
        try:
            self.start_date = s_dates[0]
            self.end_date = s_dates[1]
            log.debug(f" Parsing statements from {self.start_date} - {self.end_date}")
        except IndexError:
            log.warning(f" Dates not recognised in file name {self.f_name}")

    def parse_file(self) -> None:
        log.debug(f" Parsing statements between {self.start_date} & {self.end_date}")
        self.statement = pd.read_csv(
            f"{self.s_folder}{self.f_name}", 
            encoding='latin-1' # Account for errored entries
        )
        log.debug(f"Statement head:\n {self.statement.head()}")

class StarlingFile(ReportingFile):
    FNAME_DATE_FORMAT = r"2[0-9]{3}-[0-9]{2}-[0-9]{2}"

    def __init__(self, file_name, statements_folder):
        super().__init__(
            file_name=file_name, 
            statements_folder=statements_folder,
            file_name_date_format=self.FNAME_DATE_FORMAT
        )

class TxTableGenerator:
    BANK_NAMES = (
        "starling"
    )

    def __init__(self, bank_name, statements_folder):
        assert bank_name in self.BANK_NAMES, f"Unrecognised bank, {bank_name}"
        file_names = listdir(statements_folder)
        self.all_statements = []

        if bank_name == "starling":
            for f_name in file_names:
                sf = StarlingFile(f_name, statements_folder)
                self.all_statements.append(sf)
        else:
            return


statements_folder = "Statements/"
ttg = TxTableGenerator(
    bank_name="starling",
    statements_folder=statements_folder
)