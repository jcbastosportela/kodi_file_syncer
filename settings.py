import enum
from utils import warn
from dataclasses import dataclass
import xbmcaddon


class SettingsIds(enum.Enum):
    FIRST_TIME = enum.auto()
    MOUNT_POINT = enum.auto()
    DELETE_REMOTE = enum.auto()


@dataclass
class Settings:
    MOUNT_POINT: str = '/mnt/rpi1/'
    DELETE_REMOTE: bool = False


def load() -> Settings:
    """Loads settings

    Returns:
        Settings: Loaded settings
    """
    addon = xbmcaddon.Addon()
    s = Settings()
    try:
        s = Settings(
            addon.getSetting(SettingsIds.MOUNT_POINT.name),
            addon.getSettingBool(SettingsIds.DELETE_REMOTE.name)
        )
    except Exception:
        warn("Couldn't load settings. Using defaults")
    return s
