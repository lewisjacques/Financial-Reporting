### --- Imports --- ###

from os import listdir
import pandas as pd
import re

### --- Logging --- ###

import logging
logging.basicConfig(level=logging.NOTSET)
log = logging.getLogger('dev')
# INFO: Just info, DEBUG: Info & Debug
log.setLevel(logging.DEBUG)

### --- Filename Parsing Class --- ###

class ReportingFile:
    def __init__(self):
        return

class StarlingFile(ReportingFile):
    STMT_DATE_FORMAT = r"[0-9]{2}/[0-9]{2}/2[0-9]{3}"
    FNAME_DATE_FORMAT = r"2[0-9]{3}-[0-9]{2}-[0-9]{2}"

    def __init__(self, file_name):
        self.file_name = file_name
        self.parse_name(self.file_name)
        self.parse_file(self)

    def parse_name(self, file_name:str) -> None:
        s_dates = re.findall(self.FNAME_DATE_FORMAT, file_name)
        try:
            self.start_date = s_dates[0]
            self.end_date = s_dates[1]
        except IndexError:
            log.warning(f" Dates not recognised in file name {file_name}")

    def parse_file(self):
        log.debug(f" Parsing statements between {self.start_date} & {self.end_date}")
        statement = pd.read_csv(
            f"{statement_folder}{self.file_name}", 
            encoding='latin-1' # Account for errored entries
        )
        log.debug(f"Statement head:\n {statement.head()}")

class TxTableGenerator:
    BANK_NAMES = (
        "starling"
    )

    def __init__(self, bank_name, statement_folder):
        assert bank_name in self.BANK_NAMES, f"Unrecognised bank, {bank_name}"
        f_names = listdir(statement_folder)

        if bank_name == "starling":
            for f in f_names:
                sf = StarlingFile(f)
        else:
            return


statement_folder = "Statements/"
ttg = TxTableGenerator(
    bank_name="starling",
    statement_folder=statement_folder
)