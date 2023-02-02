import re

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
