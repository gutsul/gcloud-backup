import sqlite3


class Backup:
    id = 0
    name = None
    description = None
    count = 0
    status = False
    env = 'None'
    disk = None
    zone = None
    time = None

    def save(self):
        connection = sqlite3.connect('data/backup')
        cursor = connection.cursor()

        check_sql = "SELECT count(*) FROM backup WHERE disk = '{0}' AND zone = '{1}'".format(self.disk, self.zone)
        cursor.execute(check_sql)
        status = cursor.fetchone()[0]

        if status == 0:
            sql = "INSERT INTO backup (name, description, count, status, env, disk, zone, time) VALUES('{0}','{1}', {2}, '{3}', '{4}', '{5}', '{6}', '{7}')"\
                .format(self.name, self.description, self.count, self.status, self.env, self.disk, self.zone, self.time)
            cursor.execute(sql)

        connection.commit()
        connection.close()
