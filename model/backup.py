import sqlite3

NOT_EXIST = 0


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

        if status == NOT_EXIST:
            sql = "INSERT INTO backup (name, description, count, status, env, disk, zone, time) VALUES('{0}','{1}', {2}, '{3}', '{4}', '{5}', '{6}', '{7}')"\
                .format(self.name, self.description, self.count, self.status, self.env, self.disk, self.zone, self.time)
        else:
            sql = "UPDATE backup SET name='{0}', description='{1}', count={2}, status='{3}', env='{4}', time='{5}' WHERE id = {6}" \
                .format(self.name, self.description, self.count, self.status, self.env, self.time, self.id)

        cursor.execute(sql)

        connection.commit()
        connection.close()

    @staticmethod
    def get_all():
        connection = sqlite3.connect('data/backup')
        cursor = connection.cursor()

        sql = "SELECT id, name, description, count, status, env, disk, zone, time FROM backup"
        cursor.execute(sql)

        data = cursor.fetchall()
        connection.close()

        backups = []

        for row in data:
            backup = Backup()
            backup.id = row[0]
            backup.name = row[1]
            backup.description = row[2]
            backup.count = row[3]
            backup.status = row[4]
            backup.env = row[5]
            backup.disk = row[6]
            backup.zone = row[7]
            backup.time = row[8]
            backups.append(backup)

        return backups

    @staticmethod
    def get(id):
        connection = sqlite3.connect('data/backup')
        cursor = connection.cursor()

        sql = "SELECT id, name, description, count, status, env, disk, zone, time FROM backup WHERE id = {0}".format(id)
        cursor.execute(sql)

        data = cursor.fetchone()
        connection.close()

        if data is not None:
            backup = Backup()
            backup.id = data[0]
            backup.name = data[1]
            backup.description = data[2]
            backup.count = data[3]
            backup.status = data[4]
            backup.env = data[5]
            backup.disk = data[6]
            backup.zone = data[7]
            backup.time = data[8]
            return backup
        else:
            return None

    def delete(self):
        connection = sqlite3.connect('data/backup')
        cursor = connection.cursor()

        sql = "DELETE FROM backup WHERE id = {0}".format(self.id)
        cursor.execute(sql)

        connection.commit()
        connection.close()
