from sh import cat
from docopt import docopt


def flvcli_cmd(**kwargs):
    """
    Usage: flvcli [-h] <action>

    The most commonly used actions are:

        show                Show flexvisor server information
        create              Create flexvisor server items
        config              Config/Update or change flexvisor server configuration
        delete              Delete flexvisor server items
        assign              Assign volume or volume group to FC/iSCSI target
        unassign            Unassign volume or volume group from FC/iSCSI target
        join                Join a volume group
        leave               Leave a volume group

        map                 Display CLI assistance

    Options:

        -h, --help          show this help message and exit
    """
    print kwargs


if __name__ == "__main__":
    args = docopt(__doc__, version='flvcli version 2.5', options_first = True)
    print args

