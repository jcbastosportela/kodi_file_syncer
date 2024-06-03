import enum
from utils import warn
from dataclasses import dataclass
import xbmcaddon


class SettingsIds(enum.Enum):
    FIRST_TIME = enum.auto()
    SERIES_MOUNT_POINT = enum.auto()
    MOVIES_MOUNT_POINT = enum.auto()
    SERIES_DEST = enum.auto()
    MOVIES_DEST = enum.auto()
    DELETE_REMOTE = enum.auto()
    MOVE_REMOTE = enum.auto()


@dataclass
class Settings:
    SERIES_MOUNT_POINT:str = "/mnt/rpi1/series"
    MOVIES_MOUNT_POINT:str = "/mnt/rpi1/movies"
    SERIES_DEST:str = "/media/Portela/series"
    MOVIES_DEST:str = "/media/Seagate/movies"
    DELETE_REMOTE:str = False
    MOVE_REMOTE:str = True


def load() -> Settings:
    """Loads settings

    Returns:
        Settings: Loaded settings
    """
    addon = xbmcaddon.Addon()
    s = Settings()
    try:
        s = Settings(
            addon.getSetting(SettingsIds.SERIES_MOUNT_POINT.name),
            addon.getSetting(SettingsIds.MOVIES_MOUNT_POINT.name),
            addon.getSetting(SettingsIds.SERIES_DEST.name),
            addon.getSetting(SettingsIds.MOVIES_DEST.name),
            addon.getSettingBool(SettingsIds.DELETE_REMOTE.name),
            addon.getSettingBool(SettingsIds.MOVE_REMOTE.name)
        )
    except Exception:
        warn("Couldn't load settings. Using defaults")
    return s
