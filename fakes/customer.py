from utils.utils import get_unique_variable
from .device import Device
from .bank import Bank
import random

class Customer(object):
    def __init__(self):
        self.ktp = self.get_nik_value()
        self.test_number = get_unique_variable()
        self.email = "test+integration{}@julo.co.id".format(self.test_number)
        self.device = Device(self.test_number)
        self.bank = Bank()
        self.mobile_phone_1 = "0866{}9".format(self.test_number[3:])
        self.spouse_mobile_phone = "0866{}8".format(self.test_number[3:])
        self.kin_mobile_phone = "0866{}7".format(self.test_number[3:])
        self.pin = "159357"
        self.description = "someone account"
        self.is_own_phone = True
        self.fullname = "prod only"
        self.dob = "1992-12-12"
        self.birth_place = "Gotham City"
        self.gender = "Pria"
        self.loan_purpose = "Biaya pendidikan"
        self.loan_purpose_desc = "Need to buy new gadget to repel sharks and wanna buy a new laptop also, so i can continue playing games everyday until die"
        self.marketing_source = None
        self.payday = 20
        self.referral_code = "JULO"
        self.address_street_num = "JL. Selat Karimata 11"
        self.address_provinsi = "DKI Jakarta"
        self.address_kabupaten = "Kota Jakarta Timur"
        self.address_kecamatan = "Duren Sawit"
        self.address_kelurahan = "Duren Sawit"
        self.address_kodepos = "13440"
        self.occupied_since = "1992-12-23"
        self.home_status = "Kontrak"
        self.landlord_mobile_phone = None
        self.new_mobile_phone = None
        self.has_whatsapp_1 = False
        self.mobile_phone_2 = "0866{}6".format(self.test_number[3:])
        self.has_whatsapp_2 = None
        self.bbm_pin = None
        self.twitter_username = None
        self.instagram_username = None
        self.marital_status = "Menikah"
        self.dependent = 2
        self.spouse_name = "forgot"
        self.spouse_dob = None
        self.spouse_has_whatsapp = False
        self.kin_name = "Kate Kane"
        self.kin_dob = None
        self.kin_gender = None
        self.kin_relationship = "Saudara kandung"
        self.close_kin_name = "Eileen"
        self.close_kin_mobile_phone = "08123488950912"
        self.close_kin_relationship = None
        self.job_type = "Pegawai swasta"
        self.job_industry = "Tehnik / Computer"
        self.job_function = "do something"
        self.job_description = "Programmer / Developer"
        self.company_name = "Wayne Enterprises"
        self.company_phone_number = "021871238133"
        self.work_kodepos = "40214"
        self.job_start = "2011-12-09"
        self.monthly_income = "9999999"
        self.income_1 = 0
        self.income_2 = 0
        self.income_3 = 0
        self.last_education = "S1"
        self.college = "Gotham University"
        self.major = "Computer Engineering"
        self.graduation_year = "2015"
        self.gpa = "3.0"
        self.has_other_income = False
        self.other_income_amount = 0
        self.other_income_source = 0
        self.monthly_housing_cost = 100000
        self.monthly_expenses = 150000
        self.total_current_debt = 100000
        self.vehicle_type_1 = "Mobil"
        self.vehicle_ownership_1 = "Lunas"
        self.bank_branch = None
        self.name_in_bank = None
        self.hrd_name = None
        self.company_address = None
        self.number_of_employees = None
        self.position_employees = None
        self.employment_status = None
        self.billing_office = None
        self.mutation = None
        self.dialect = None
        self.mother_maiden_name = "mom"

    def get_nik_value(self):
        unique_variable = get_unique_variable()
        nik_prefix = unique_variable[:6]
        nik_suffix = unique_variable[6:]
        nik_format = "{}711299{}".format(nik_prefix, nik_suffix)
        nik = ""
        for digit in nik_format:
            if len(nik) != 0 and nik[-1] == "0" and digit == "0":
                nik += str(random.randint(1, 9))
                continue
            nik += digit

        while len(nik) < 16:
            nik += "1"

        return nik

    def generate_form_submission_params(self, **kwargs):

        form_submission_data = {
            "fullname": self.fullname,
            "dob": self.dob,
            "birth_place": self.birth_place,
            "gender": self.gender,
            "loan_purpose": self.loan_purpose,
            "loan_purpose_desc": self.loan_purpose_desc,
            "payday": self.payday,
            "referral_code": self.referral_code,
            "marital_status": self.marital_status,
            "address_street_num": self.address_street_num,
            "address_provinsi": self.address_provinsi,
            "address_kabupaten": self.address_kabupaten,
            "address_kecamatan": self.address_kecamatan,
            "address_kelurahan": self.address_kelurahan,
            "address_kodepos": self.address_kodepos,
            "occupied_since": self.occupied_since,
            "home_status": self.home_status,
            "mobile_phone_2": self.mobile_phone_2,
            "dependent": self.dependent,
            "spouse_has_whatsapp": self.spouse_has_whatsapp,
            "kin_name": self.kin_name,
            "kin_mobile_phone": self.kin_mobile_phone,
            "kin_relationship": self.kin_relationship,
            "job_type": self.job_type,
            "job_industry": self.job_industry,
            "job_function": self.job_function,
            "job_description": self.job_description,
            "company_name": self.company_name,
            "company_phone_number": self.company_phone_number,
            "job_start": self.job_start,
            "monthly_income": self.monthly_income,
            "last_education": self.last_education,
            "monthly_housing_cost": self.monthly_housing_cost,
            "monthly_expenses": self.monthly_expenses,
            "total_current_debt": self.total_current_debt,
            "bank_name": self.bank.name,
            "name_in_bank": self.name_in_bank,
            "application_number": 1,
            "ktp": self.ktp,
            "mother_maiden_name": self.mother_maiden_name,
            "is_term_accepted": True,
            "is_verification_agreed": True,
            "teaser_loan_amount": 100000,
            "address_same_as_ktp": True,
            "application_status": 100,
            "mobile_phone_1": self.mobile_phone_1,
            "bank_account_number": self.bank.account_number,
        }

        for key, value in kwargs.items():

            if key == "fullname":
                form_submission_data["name_in_bank"] = value
            if key == "province":
                form_submission_data["address_provinsi"] = kwargs["province"]
                form_submission_data["address_kabupaten"] = kwargs["cities"]
                form_submission_data["address_kecamatan"] = kwargs["districts"]
                form_submission_data["address_kelurahan"] = kwargs["subdistricts"]
            if key == "short_form" and value == True:
                form_submission_data["email"] = self.email
                form_submission_data.pop("loan_purpose_desc")
                form_submission_data.pop("mobile_phone_1")
            if key == "marital_status":
                form_submission_data["marital_status"] = kwargs["marital_status"]
            if key == "device_id":
                form_submission_data["device"] = kwargs["device_id"]

        if form_submission_data["marital_status"] == "Menikah":
            form_submission_data["spouse_name"] = self.spouse_name
            form_submission_data[
                "spouse_mobile_phone"
            ] = self.spouse_mobile_phone
        else:
            form_submission_data["close_kin_name"] = self.close_kin_name
            form_submission_data[
                "close_kin_mobile_phone"
            ] = self.close_kin_mobile_phone

        return form_submission_data