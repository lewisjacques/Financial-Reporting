from reporting_file import ReportingFile

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
