from reporting_file import ReportingFile

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
