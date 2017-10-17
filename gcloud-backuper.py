#!/usr/bin/env python3
import argparse
import googleapiclient.discovery
from prettytable import PrettyTable
from model.backup import Backup


# Global settings
PROJECT_ID = 'adlithium-1289'


def create_service():
    # Construct the service object for interacting with the Cloud Storage API -
    # the 'storage' service, at version 'v1'.
    # Authentication is provided by application default credentials.
    # When running locally, these are available after running
    # `gcloud auth application-default login`. When running on Compute
    # Engine, these are available from the environment.
    return googleapiclient.discovery.build('compute', 'v1')


def validate_disk(disk, zone):
    try:
        request = service.disks().get(project=PROJECT_ID, zone=zone, disk=disk)
        response = request.execute()
        return response
    except:
        return None


def add_backup(args):
    # TODO: Maybe_delete
    disk = str(args.disk)
    zone = str(args.zone)

    response = validate_disk(disk, zone)
    if response is None:
        print("ERROR: Name or zone is not valid.")
        exit(0)

    backup = Backup()
    backup.disk = disk
    backup.zone = zone
    backup.save()

    print("Saved: {}".format(backup.disk))


def remove_backup(args):
    id = int(args.id)
    Backup.delete(id)
    print("Removed backup: {0}".format(id))


def print_list(args):

    backups = Backup().get_all()

    table = PrettyTable(['ID', 'Name', 'Disk', 'Time (UTC)', 'Zone', 'Environment', 'Count', 'Status'])


    for backup in backups:
        table.add_row([backup.id, backup.name, backup.disk, backup.time,
                       backup.zone, backup.env, backup.count, backup.status])

    print(table)


def parse_args():
    parser = argparse.ArgumentParser(description='GCloud backup utility')
    subparsers = parser.add_subparsers()

    parser_append = subparsers.add_parser('append', help='Append a persistent disk to backup list.')
    parser_append.add_argument('disk', help='The name of persistent disk.')
    parser_append.add_argument('zone', help='The name of the zone.')
    parser_append.set_defaults(func=add_backup)

    parser_remove = subparsers.add_parser('remove', help='Remove a persistent disk from backup list.')
    parser_remove.add_argument('id', help='Id of persistent disk.')
    parser_remove.set_defaults(func=remove_backup)


    parser_list = subparsers.add_parser('list', help='Show backup list')
    parser_list.set_defaults(func=print_list)



    return parser.parse_args()


def main():
    args = parse_args()
    args.func(args)


if __name__ == '__main__':
    service = create_service()
    main()
