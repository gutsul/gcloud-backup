#!/usr/bin/env python3
import argparse
import googleapiclient.discovery
from pprint import pprint
from model.disk import Disk


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


def validate_disk(name, zone):
    try:
        request = service.disks().get(project=PROJECT_ID, zone=zone, disk=name)
        response = request.execute()
        return response
    except:
        return None


def create_new_disk(args):
    # TODO: Maybe_delete
    name = str(args.name)
    zone = str(args.zone)

    response = validate_disk(name, zone)
    if response is None:
        print("ERROR: Name or zone is not valid.")
        exit(0)

    disk = Disk()
    disk.name = name
    disk.zone = zone
    disk.sizeGb = response.get('sizeGb')

    print("Added: {}".format(disk.name))
    # pprint(response)


def print_list(args):
    print("List")


def parse_args():
    parser = argparse.ArgumentParser(description='GCloud backup utility')
    subparsers = parser.add_subparsers()

    parser_append = subparsers.add_parser('append', help='Append a persistent disk to backup list')
    parser_append.add_argument('name', help='The name of persistent disk')
    parser_append.add_argument('zone', help='The name of the zone')
    parser_append.set_defaults(func=create_new_disk)

    parser_list = subparsers.add_parser('list', help='Show backup list')
    parser_list.set_defaults(func=print_list)

    return parser.parse_args()


def main():
    args = parse_args()
    args.func(args)


if __name__ == '__main__':
    service = create_service()
    main()
