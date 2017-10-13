import sqlite3


class Disk:
    id = 0
    name = None
    zone = None
    sizeGb = 0

    def save(self):
        connection = sqlite3.connect('data/backup')
        cursor = connection.cursor()

        check_sql = "SELECT count(*) FROM disks WHERE name = '{0}' AND zone = '{1}'".format(self.name, self.zone)
        cursor.execute(check_sql)
        status = cursor.fetchone()[0]

        if status == 0:
            sql = "INSERT INTO disks (name, zone, size_gb) VALUES('{0}', '{1}', {2})".format(self.name, self.zone, self.sizeGb)
            cursor.execute(sql)

        connection.commit()
        connection.close()
