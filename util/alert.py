from playsound import playsound
from pathlib import Path
from smtplib import SMTP

from model.accountLoginDetails import AccountLoginDetails


class Alert:
    @staticmethod
    def create_noise():
        file_parent = str(Path(__file__).parent.absolute())
        path: str = str(Path(file_parent + "/sound.wav"))
        for _ in range(4):
            playsound(path)

    @staticmethod
    def send_email(from_account: AccountLoginDetails, to_email: str, subject: str, msg: str):
        server = SMTP("smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        server.login(from_account.email, from_account.password)
        message = f"Subject: {subject}\n\n{msg}"
        server.sendmail(from_addr=from_account.email,
                        to_addrs=to_email,
                        msg=message)
        server.quit()