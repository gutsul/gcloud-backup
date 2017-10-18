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
    backup.name = "{0}-{1}".format(disk, backup.count)
    backup.disk = disk
    backup.zone = zone
    backup.save()

    print("Backup added: {}".format(backup.disk))


def remove_backup(args):
    id = int(args.id)
    backup = Backup.get(id)

    try:
        snapshot = backup.name
        # TODO: check it
        api.delete_snapshot(snapshot)
        backup.delete()
        print("Removed backup: {0}".format(snapshot))
    except:
        print("Backup with id {0} not exist.".format(id))


def show_backups(args):
    backups = Backup().get_all()

    table = PrettyTable(['ID', 'Name', 'Description', 'Disk', 'Zone', 'Environment'])

    for backup in backups:
        table.add_row([backup.id, backup.name, backup.description, backup.disk,
                       backup.zone, backup.env])

    print(table)


def configure_backup(args):
    id = int(args.id)
    backup = Backup.get(id)

    print("Configure backup")
    print("Disk: {}".format(backup.disk))
    print("Zone: {}".format(backup.zone))
    print("-----------------------------------")

    default_description = "None"
    backup.description = configure(default_description, "Description")

    default_env = "Development"
    backup.env = configure(default_env, "Environment")

    # TODO: ADD check time format
    # default_time = "04:00"
    # backup.time = configure(default_time, "Time")

    # TODO: Add enable/disable setting

    backup.save()


def configure(default, title):
    EMPTY = ""

    value = input("{1} [default:{0}]: ".format(default, title))
    if value == EMPTY:
        setting = default
    else:
        setting = value

    return setting


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
