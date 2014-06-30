from collections import OrderedDict

class CommandNode(object):
    parser = None
    subparsers= None

    def __init__(self, name, pattern, parent = None):
        self.name = name
        self.parent = parent
        self.pattern = pattern

        if self.parent != None:
            self.level = parent.level + 1
        else:
            self.level = 1

        self.subcmds = OrderedDict()

    def __getitem__(self, subcmd_name):

        if subcmd_name not in self.subcmds:
            self.subcmds[subcmd_name] = CommandNode(subcmd_name, self)

        return self.subcmds[subcmd_name]

    def dump_command_path(self):
        parent = self.parent
        full_path = [self.name]

        while parent is not None:
            full_path.append(parent.name)
            parent = parent.parent

        return " ".join(reversed(full_path))

    def generate_parser(self, parent_subparsers = None):
        pass

    def traversal(self, func):
        func(self)

        for name, cmd in self.subcmds:
            cmd.traversal(func)

    def is_leaf(self):
        return len(self.subcmds) == 0

