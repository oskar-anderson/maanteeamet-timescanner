import io
import yaml
from typing import *

from model.available_reservation import Reservation

def getConfig(name: str) -> dict:
    try:
        file = io.open(name, mode="r", encoding="utf-8")
        try:
            json_out = yaml.load(file, Loader=yaml.Loader)
            file.close()
            return json_out
        except yaml.YAMLError as exc:
            print(f"File '{name}' cannot be read. Json cannot be parsed. {exc}")
    except OSError:
        print(f"File {name} cannot be opened. Does it exist?")
    exit()



def parse_list_times(list_times_raw: List[str]) -> List[Reservation]:
    list_times: List[Reservation] = [
        Reservation(
            date=x.split(" ")[0],
            time=x.split(" ")[1],
            place=x.split(" ")[2]
        ) for x in list_times_raw
    ]
    return list_times