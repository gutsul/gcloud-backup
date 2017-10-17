#!/usr/bin/env python3
import argparse

from prettytable import PrettyTable
from model.backup import Backup
import api


def add_backup(args):
    disk = str(args.disk)
    zone = str(args.zone)

    api.check_disk(disk, zone)

    backup = Backup()
    backup.disk = disk
    backup.zone = zone
    backup.save()

    print("Backup added: {}".format(backup.disk))


def remove_backup(args):
    id = int(args.id)
    Backup.delete(id)
    print("Removed backup: {0}".format(id))


def show_backups(args):
    backups = Backup().get_all()

    table = PrettyTable(['ID', 'Name', 'Disk', 'Time (UTC)', 'Zone', 'Environment', 'Status'])

    for backup in backups:
        table.add_row([backup.id, backup.name, backup.disk, backup.time,
                       backup.zone, backup.env, backup.status])

    print(table)


def configure_backup(args):
    id = int(args.id)
    backup = Backup.get(id)

    print("Configure backup")
    print("Disk: {}".format(backup.disk))
    print("Zone: {}".format(backup.zone))
    print("-----------------------------------")

    # name = input("Backup ")




def parse_args():
    parser = argparse.ArgumentParser(description='GCloud backup utility')
    subparsers = parser.add_subparsers()

    parser_append = subparsers.add_parser('append', help='Append a persistent disk to backup list.')
    parser_append.add_argument('disk', help='The name of persistent disk.')
    parser_append.add_argument('zone', help='The name of the zone.')
    parser_append.set_defaults(func=add_backup)

    parser_remove = subparsers.add_parser('remove', help='Remove a persistent disk from backup list.')
    parser_remove.add_argument('id', help='Backup ID.')
    parser_remove.set_defaults(func=remove_backup)

    parser_configure = subparsers.add_parser('configure', help='Configure backup.')
    parser_configure.add_argument('id', help='Backup ID.')
    parser_configure.set_defaults(func=configure_backup)

    parser_list = subparsers.add_parser('list', help='Show backup list')
    parser_list.set_defaults(func=show_backups)

    return parser.parse_args()


def main():
    args = parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
