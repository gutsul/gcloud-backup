from model.disk import Disk


class Backup:
    disk = Disk()
    cron = None
    delete_old = True
    enable = False
