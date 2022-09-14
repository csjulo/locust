import os
from utils.utils import get_unique_variable

class Bank(object):
    def __init__(self):
        self.test_number = get_unique_variable()
        self.name = "BANK MANDIRI (PERSERO), Tbk"
        self.other_bank_name = "Mandiri"
        self.account_number = (
            self.test_number if "BCA" in self.name else self.test_number + "6969"
        )
        # self.mock_account_number = (
        #     "5600412088" if os.environ["ENVIRONMENT"] == "staging" else "51163752756969"
        # )
        # self.mock_name_validation_id = (
        #     41104 if os.environ["ENVIRONMENT"] == "staging" else 14522
        # )
        # self.other_bank_account = self.test_number + "9696"
