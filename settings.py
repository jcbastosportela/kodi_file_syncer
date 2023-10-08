import enum
import json
from utils import *
from dataclasses import dataclass


FILE_NAME = 'settings.json'


class SettingsIds(enum.Enum):
    FIRST_TIME = enum.auto()
    MOUNT_POINT = enum.auto()


@dataclass
class Settings:
    MOUNT_POINT:str = '/mnt/rpi1/'

def save(settings:Settings)->None:
    with open(FILE_NAME, 'w') as f:
        json.dump(settings, f, indent=4)

def load()->Settings:
    s = Settings()
    try:
        with open(FILE_NAME, 'r') as f:
            settings_dic = json.load(f)
        s = Settings(settings_dic[SettingsIds.MOUNT_POINT.name])
    except Exception as ex:
        warn("Couldn't load settings. Using defaults")
    return s