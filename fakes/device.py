class Device(object):
    def __init__(self, test_number):
        self.android_id = "apitest{}".format(test_number)
        self.gcm_reg_id = "apitest{}".format(test_number)
        self.manufacturer = "Android"
        self.model = "Google"
        self.longitude = "106.91328"
        self.latitude = "-6.23619"
        self.app_version = AppVersion()

class AppVersion(object):
    def __init__(self):
        self.long_form = "6.5.0"
        self.short_form = "7.2.0"
