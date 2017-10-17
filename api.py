from time import sleep

from googleapiclient import discovery

# Constants:
SNAPSHOT_READY = 'READY'
PROJECT_ID = 'adlithium-1289'


service = discovery.build('compute', 'v1')


def check_disk(disk, zone):
    try:
        request = service.disks().get(project=PROJECT_ID, zone=zone, disk=disk)
        request.execute()
    except:
        print("ERROR: Name or zone is not valid.")
        exit(0)


def create_snapshot(name, description, disk, zone):
    snapshot_body = {
        "name": name,
        "description": description,
    }

    request = service.disks().createSnapshot(project=PROJECT_ID, zone=zone, disk=disk, body=snapshot_body)
    request.execute()

    check_snapshot_status(name)


def check_snapshot_status(name):
    while True:
        sleep(20)

        request = service.snapshots().get(project=PROJECT_ID, snapshot=name)
        response = request.execute()

        status = response.get('status')

        if status == SNAPSHOT_READY:
            print("Snapshot {0} created".format(name))
            break


def delete_snapshot(name):
    request = service.snapshots().delete(project=PROJECT_ID, snapshot=name)
    request.execute()
