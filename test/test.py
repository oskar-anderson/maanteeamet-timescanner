import datetime
import unittest
from typing import *


from model.available_reservation import Reservation
from model.accountLoginDetails import AccountLoginDetails
import schedule_checker as sc
import util
from util.alert import Alert
from util import constants, helper


def sound():
    Alert.create_noise()

def email_sending():
    userdata: dict = helper.getConfig(constants.UserData.FILE_NAME)
    acc: AccountLoginDetails = AccountLoginDetails(
        email=userdata[constants.UserData.SENDER_EMAIL_ADDRESS],
        password=userdata[constants.UserData.SENDER_PASSWORD]
    )
    email = userdata[constants.UserData.RECEIVER_EMAIL]
    Alert.send_email(
        from_account=acc,
        to_email=email,
        subject="Mail check",
        msg="This is a test to see if automated mailing works."
    )


class TestMethods(unittest.TestCase):

    good_cities: List[str] = ["Rakvere", "Tallinn", "Haapsalu"]
    date_before: datetime = datetime.datetime(year=2019, month=12, day=31)

    def test_good_times(self):
        print(TestMethods.test_good_times.__name__)
        dataset1: List[str] = [
            "03.12.2019 14:30 Tallinn",
            "16.12.2019 09:00 Tartu",
            "17.12.2019 15:45 Kuressaare",
            "18.12.2019 09:00 Viljandi",
            "18.12.2019 11:30 Pärnu",
            "27.12.2019 13:15 Võru",
            "02.01.2020 14:30 Rakvere",
            "08.01.2020 09:00 Paide",
            "09.01.2020 13:15 Haapsalu",
            "15.01.2020 11:30 Narva",
            "16.01.2020 10:15 Jõhvi"
        ]

        dataset2: List[str] = [
            "02.12.2019 14:30 Rakvere",
            "16.12.2019 09:00 Tartu",
            "17.12.2019 15:45 Kuressaare",
            "18.12.2019 09:00 Viljandi",
            "18.12.2019 11:30 Pärnu",
            "27.12.2019 13:15 Võru",
            "03.01.2020 14:30 Tallinn",
            "08.01.2020 09:00 Paide",
            "09.01.2020 13:15 Haapsalu",
            "15.01.2020 11:30 Narva",
            "16.01.2020 10:15 Jõhvi"
        ]

        old_times: List[Reservation] = []

        times = util.helper.parse_list_times(dataset1)
        found_time1 = next(iter(sc.find_good_times(
            good_cities=self.good_cities,
            before_date=self.date_before,
            times=times,
            old_good_times=old_times
        )), None)
        found_time1_comparison = Reservation(
            date="03.12.2019",
            time="14:30",
            place="Tallinn"
        )
        self.assertTrue(found_time1 == found_time1_comparison)
        old_times.append(found_time1)

        times = util.helper.parse_list_times(dataset2)
        found_time2 = next(iter(sc.find_good_times(
            good_cities=self.good_cities,
            before_date=self.date_before,
            times=times,
            old_good_times=old_times
        )), None)
        found_time2_comparison = Reservation(
            date="02.12.2019",
            time="14:30",
            place="Rakvere"
        )
        self.assertTrue(found_time2 == found_time2_comparison)
        old_times.append(found_time2)
        times = util.helper.parse_list_times(dataset1)
        found_time3 = next(iter(sc.find_good_times(
            good_cities=self.good_cities,
            before_date=self.date_before,
            times=times,
            old_good_times=old_times
        )), None)
        self.assertTrue(found_time3 is None)

        times = util.helper.parse_list_times(dataset2)
        found_time4 = next(iter(sc.find_good_times(
            good_cities=self.good_cities,
            before_date=self.date_before,
            times=times,
            old_good_times=old_times
        )), None)
        self.assertTrue(found_time4 is None)


def main():
    pass
    sound()
    # email_sending()
    TestMethods().test_good_times()

if __name__ == '__main__':
    main()