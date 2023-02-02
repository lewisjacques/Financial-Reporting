### --- Imports --- ###

from Banks.starling import StarlingFile
from Banks.natwest import NatwestFile

from os import listdir
import pandas as pd
import re

### --- Logging --- ###

import logging
logging.basicConfig(level=logging.NOTSET)
log = logging.getLogger('dev')
# INFO: Just info, DEBUG: Info & Debug
log.setLevel(logging.INFO)

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