from sh import echo

def echo_hello_world_cmd(**kwargs):
    """
    Usage:
        echo hello world --user <user> <target> [--chinese (yes|no)]

    Options:
        --user <user>             Hello World [default: root]
        -c,--chinese                 Use Chinese to say hello world
    """
    print echo("echo hello world:" + kwargs["user"])

class echo_hello_world2_cmd(object):
    """
    Usage:
        echo hello world2 --user <user>

    Options:
        --user <user>             Hello World [default: root]
    """

    def __call__(self, **kwargs):
        print echo("echo hello world2:" + kwargs["user"])


if __name__ == "__main__":
    echo_hello_world_cmd(**{"user":"TestCase"})

