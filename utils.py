import xbmc
import xbmcaddon

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')

def info(msg):
    xbmc.log(f'{addonname} - {msg}' , level=xbmc.LOGINFO)
def debug(msg):
    xbmc.log(f'{addonname} - {msg}' , level=xbmc.LOGDEBUG)
def error(msg):
    xbmc.log(f'{addonname} - {msg}' , level=xbmc.LOGERROR)
def warn(msg):
    xbmc.log(f'{addonname} - {msg}' , level=xbmc.LOGWARNING)