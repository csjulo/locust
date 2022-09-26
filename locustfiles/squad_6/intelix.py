from locust import task, constant, SequentialTaskSet, FastHttpUser, LoadTestShape, TaskSet, tag
from locust_plugins.csvreader import CSVReader
from locust.exception import StopUser
from json import JSONDecodeError
import random
from fakes.constant import app_version, registration
from fakes.customer import Customer as customers

# Get data parameterization from CSV
test_data = CSVReader("CSV_Data//registration_long_form.csv")

class OnboardingFeature(SequentialTaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.token = ""
        self.application_id = ""
        self.nik = ""
        self.email = ""
        self.image_id = ""
        self.province = ""
        self.city = ""
        self.district = ""
        self.sub_district = ""
        self.device_id = ""

    @task
    def set_initial_data(self):
        data_csv = next(test_data)
        self.loan_id = data_csv[0]
        self.payment_id = data_csv[1]
        self.account_id = data_csv[2]
        self.account_payment_id = data_csv[3]
        self.is_j1 = data_csv[4]
        self.customer_id = data_csv[5]
        self.application_id = data_csv[6]
        self.nama_customer = data_csv[7]
        self.mobile_phone_1 = data_csv[8]
        self.mobile_phone_2 = data_csv[9]
        self.nama_perusahaan = data_csv[10]
        self.posisi_karyawan = data_csv[11]
        self.telp_perusahaan = data_csv[12]
        self.dpd = data_csv[13]
        self.angsuran_per_bulan = data_csv[14]
        self.denda = data_csv[15]
        self.outstanding = data_csv[15]
        self.tanggal_jatuh_tempo = data_csv[16]
        self.nama_pasangan = data_csv[17]
        self.no_telp_pasangan = data_csv[18]
        self.nama_kerabat = data_csv[19]
        self.no_telp_kerabat = data_csv[20]
        self.hubungan_kerabat = data_csv[21]
        self.alamat = data_csv[22]
        self.kota = data_csv[23]
        self.jenis_kelamin = data_csv[24]
        self.tgl_lahir = data_csv[25]
        self.tgl_gajian = data_csv[26]
        self.tujuan_pinjaman = data_csv[27]
        self.tgl_upload = data_csv[28]
        self.va_bca = data_csv[29]
        self.va_permata = data_csv[30]
        self.va_maybank = data_csv[31]
        self.va_alfamart = data_csv[32]
        self.va_indomaret = data_csv[33]
        self.campaign = data_csv[34]
        self.tipe_produk = data_csv[35]
        self.jumlah_pinjaman = data_csv[36]
        self.last_pay_date = data_csv[37]
        self.last_pay_amount = data_csv[38]
        self.status_tagihan_1 = data_csv[39]
        self.status_tagihan_2 = data_csv[40]
        self.status_tagihan_3 = data_csv[41]
        self.status_tagihan_4 = data_csv[42]
        self.status_tagihan_5 = data_csv[43]
        self.status_tagihan_6 = data_csv[44]
        self.status_tagihan_7 = data_csv[45]
        self.status_tagihan_8 = data_csv[46]
        self.status_tagihan_9 = data_csv[47]
        self.status_tagihan_10 = data_csv[48]
        self.status_tagihan_11 = data_csv[49]
        self.status_tagihan_12 = data_csv[50]
        self.status_tagihan_13 = data_csv[51]
        self.status_tagihan_14 = data_csv[52]
        self.status_tagihan_15 = data_csv[53]
        self.partner_name = data_csv[54]
        self.last_agent = data_csv[55]
        self.last_call_status = data_csv[56]
        self.refinancing_status = data_csv[57]
        self.activation_amount = data_csv[58]
        self.program_expiry_date = data_csv[59]
        self.customer_bucket_type = data_csv[60]
        self.promo_untuk_customer = data_csv[61]
        self.zipcode = data_csv[62]
        self.dpd = data_csv[63]
        self.bucket = data_csv[64]
    
    @task
    def intelix(self):
        endpoint = "https://rnd.ecentrix.net/ecx_ws/"
        name_thread = "intelix - " + endpoint
        data = {
            "loan_id": self.loan_id,
            "payment_id": (self.payment_id),
            "account_id": (self.account_id),
            "account_payment_id": (self.account_payment_id),
            "is_j1": (self.is_j1),
            "customer_id": (self.customer_id),
            "application_id": (self.application_id),
            "nama_customer": (self.nama_customer),
            "mobile_phone_1": (self.mobile_phone_1),
            "mobile_phone_2": (self.mobile_phone_2),
            "nama_perusahaan": (self.nama_perusahaan),
            "posisi_karyawan": (self.posisi_karyawan),
            "telp_perusahaan": (self.telp_perusahaan),
            "dpd": (self.dpd),
            "angsuran_per_bulan": (self.angsuran_per_bulan),
            "denda": (self.denda),
            "outstanding": (self.outstanding),
            "tanggal_jatuh_tempo": (self.tanggal_jatuh_tempo),
            "nama_pasangan": (self.nama_pasangan),
            "no_telp_pasangan": (self.no_telp_pasangan),
            "nama_kerabat": (self.nama_kerabat),
            "no_telp_kerabat": (self.no_telp_kerabat),
            "hubungan_kerabat": (self.hubungan_kerabat),
            "alamat": (self.alamat),
            "kota": (self.kota),
            "jenis_kelamin": (self.jenis_kelamin),
            "tgl_lahir": (self.tgl_lahir),
            "tgl_gajian": (self.tgl_gajian),
            "tujuan_pinjaman": (self.tujuan_pinjaman),
            "tgl_upload": (self.tgl_uploadv
            "va_bca": (self.va_bca),
            "va_permata": (self.va_permata),
            "va_maybank": (self.va_maybank),
            "va_alfamart": (self.va_alfamart),
            "va_indomaret": (self.va_indomaret),
            "campaign": (self.campaign),
            "tipe_produk": (self.tipe_produk),
            "jumlah_pinjaman": (self.jumlah_pinjaman),
            "last_pay_date": (self.last_pay_date),
            "last_pay_amount": (self.last_pay_amount),
            "status_tagihan_1": (self.status_tagihan_1),
            "status_tagihan_2": (self.status_tagihan_2),
            "status_tagihan_3": (self.status_tagihan_3),
            "status_tagihan_4": (self.status_tagihan_4),
            "status_tagihan_5": (self.status_tagihan_5),
            "status_tagihan_6": (self.status_tagihan_6),
            "status_tagihan_7": (self.status_tagihan_7),
            "status_tagihan_8": (self.status_tagihan_8),
            "status_tagihan_9": (self.status_tagihan_9),
            "status_tagihan_10": (self.status_tagihan_10),
            "status_tagihan_11": (self.status_tagihan_11),
            "status_tagihan_12": (self.status_tagihan_12),
            "status_tagihan_13": (self.status_tagihan_13),
            "status_tagihan_14": (self.status_tagihan_14),
            "status_tagihan_15": (self.status_tagihan_15),
            "partner_name": (self.partner_name),
            "last_agent": (self.last_agent),
            "last_call_status": (self.last_call_status),
            "refinancing_status": (self.refinancing_status),
            "activation_amount": (self.activation_amount),
            "program_expiry_date": (self.program_expiry_date),
            "customer_bucket_type": (self.customer_bucket_type),
            "promo_untuk_customer": (self.promo_untuk_customer),
            "zipcode": (self.zipcode),
            "dpd": (self.dpd),
            "bucket": (self.bucket)
        }

        with self.client.post(
            endpoint,
            catch_response=True,
            name=name_thread,
            data=data,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Failure in check strong pin")

class MySeqTest(FastHttpUser):
    wait_time = constant(1)
    host = "https://api-staging.julofinance.com"
    tasks = [OnboardingFeature]

# class StagesShape(LoadTestShape):
#     stages = [
#         #### Load Test ####
#         {"duration": 60, "users": 35, "spawn_rate": 5}, # simulate ramp-up of traffic to 50 users over 25 seconds.
#         {"duration": 75, "users": 10, "spawn_rate": 5}, # simulate ramp-up of traffic to 50 users over 25 seconds.
#         {"duration": 85, "users": 1, "spawn_rate": 1}, # stay at 50 users for around 15 seconds

#         #### Stress Test ####
#         # {"duration": 25, "users": 1, "spawn_rate": 1}, # simulate ramp-up of traffic to 50 users over 15 seconds. (normal load)
#         # {"duration": 40, "users": 5, "spawn_rate": 1}, # stay at 50 users for around 20 seconds
#         # {"duration": 45, "users": 75, "spawn_rate": 20}, # ramp-up to 60 users around 15 seconds (beyond the breaking point)
#         # {"duration": 60, "users": 30, "spawn_rate": 10}, # ramp-down
#         # {"duration": 75, "users": 10, "spawn_rate": 10}, # ramp-down
#         # {"duration": 90, "users": 1, "spawn_rate": 1} # ramp-down to 1 users
        
#         #### Spike Test ####
#         # {"duration": 10, "users": 20, "spawn_rate": 5}, # simulate ramp-up of traffic to 20 users over 10 seconds. (normal load)
#         # {"duration": 35, "users": 100, "spawn_rate": 100}, # stay at 100 users for around 10 seconds
#         # {"duration": 45, "users": 20, "spawn_rate": 20}, # ramp-down to 50 users around 20 seconds (recovery)
#         # {"duration": 55, "users": 10, "spawn_rate": 10}, # ramp-down
#         # {"duration": 65, "users": 1, "spawn_rate": 1} # ramp-down to 1 users
#     ]

#     def tick(self):
#         run_time = self.get_run_time()

#         for stage in self.stages:
#             if run_time < stage["duration"]:
#                 tick_data = (stage["users"], stage["spawn_rate"])
#                 return tick_data

#         return None
