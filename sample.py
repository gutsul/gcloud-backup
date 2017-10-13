import argparse
from pprint import pprint

import googleapiclient.discovery


def create_service():
    # Construct the service object for interacting with the Cloud Storage API -
    # the 'storage' service, at version 'v1'.
    # Authentication is provided by application default credentials.
    # When running locally, these are available after running
    # `gcloud auth application-default login`. When running on Compute
    # Engine, these are available from the environment.
    return googleapiclient.discovery.build('compute', 'v1')


def list_disks(service, project_id):
    zone = 'us-central1-c'

    request = service.disks().list(project=project_id, zone=zone)
    while request is not None:
        response = request.execute()

        for disk in response['items']:
            # TODO: Change code below to process each `disk` resource:
            pprint(disk)

        request = service.disks().list_next(previous_request=request, previous_response=response)


def main(project_id):
    service = create_service()
    list_disks(service, project_id)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(
    #     description=__doc__,
    #     formatter_class=argparse.RawDescriptionHelpFormatter)
    # parser.add_argument('project_id', help='Your Google Cloud Project ID.')
    #
    # args = parser.parse_args()

    # main(args.project_id)

    project_id = 'adlithium-1289'
    main(project_id)
