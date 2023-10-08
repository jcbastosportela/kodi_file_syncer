#!/usr/bin/env python
__author__ = "Joao Carlos Bastos Portela"
__copyright__ = "left"
__license__ = "GPL"
__version__ = "0.0.2"
__email__ = "jcbastosportela@gmail.com"

import time
import xbmc
import settings
from settings import SettingsIds, Settings
from utils import *
import subprocess
import os


CHECK_PERDIOD = 60 #s


def _sync_and_clean(remote, local)->None:
    try:
        cmd = ['rsync','-avzh', remote+'/', local+'/']
        ret = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        info(f'Return code {ret}')
        debug(f'stdout ->\n {ret.stdout}\nstderr ->\n {ret.stderr}')
        if ret.returncode == 0 :
            ret = subprocess.run(f'rm -rf {remote}/*', shell=True)
            info(ret)
    except Exception as ex:
        error(f"Failed to execute rsync. Error {ex}")


if __name__ == '__main__':
    monitor = xbmc.Monitor()
    
    s = settings.load()
    info(f"The server address is {s.MOUNT_POINT}")
    remote_movies_path = os.path.abspath(os.path.join(s.MOUNT_POINT, 'movies/'))
    local_movies_path = os.path.abspath('/media/Portela/movies/')
    remote_series_path = os.path.abspath(os.path.join(s.MOUNT_POINT, 'series/'))
    local_series_path = os.path.abspath('/media/Portela/series/')

    while not monitor.abortRequested():
        info("Going to rsync %s" % time.time())
        _sync_and_clean(remote_movies_path, local_movies_path)
        _sync_and_clean(remote_series_path, local_series_path)
        info('Done rsyncing')
        
        # Sleep/wait for abort for CHECK_PERDIOD seconds
        if monitor.waitForAbort(CHECK_PERDIOD):
            # Abort was requested while waiting. We should exit
            break
    info("Leaving")