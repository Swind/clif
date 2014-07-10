import sys
import pkgutil
import inspect
import docopt_lite

import logging
logger = logging.getLogger(__name__)

from command import CommandNode


def load_all_modules_from_dir(dirname):

    modules = []

    for importer, package_name, _ in pkgutil.iter_modules([dirname]):
        if package_name not in sys.modules:
            module = importer.find_module(package_name).load_module(package_name)
            modules.append(module)

    return modules


def load_modules(folders):
    modules_list = map(lambda folder: load_all_modules_from_dir(folder), folders)

    def flat_list(result, items):
        result.extend(items)
        return result

    modules = reduce(flat_list, modules_list, [])

    return modules


def get_cmd_funcs(cmd_modules, cmd_suffix):

    #Return all function or class in the module and the suffix of name is <cmd_suffix>
    def find_cmd_funcs(funcs, cmd_module):
        cmd_funcs = [cmd_func for (cmd_name, cmd_func) in inspect.getmembers(cmd_module) if cmd_name.endswith(cmd_suffix)]
        funcs.extend(cmd_funcs)
        return funcs

    return reduce(find_cmd_funcs, cmd_modules, [])


class CLIF(object):

    def __init__(self, prog_name, cmd_folders, cmd_suffix="_cmd"):

        if type(cmd_folders) is str:
            folders = [cmd_folders]
        else:
            folders = cmd_folders

        self.root_cmd = CommandNode(prog_name, pattern=None, parent=None)

        self.__load_cmds(folders, cmd_suffix)

    def __load_cmds(self, folders, cmd_suffix):

        cmd_modules = load_modules(folders)
        cmd_funcs = get_cmd_funcs(cmd_modules, cmd_suffix)

        for cmd_func in cmd_funcs:

            logger.debug("Find command function or class %s" % cmd_func.__name__)

            if inspect.isclass(cmd_func):
                #If the command if a class, create a command class instance
                cmd_func = cmd_func()

            #Get doc string in the command
            doc = inspect.getdoc(cmd_func)

            #Parse the doc string and generate docopt pattern
            pattern = docopt_lite.build_docopt_pattern(doc)

            self.root_cmd = self.__build_command_node(pattern, self.root_cmd)

    def __build_command_node(self, pattern, parent_cmd):
        #Remove Required(Required(....))
        pattern = pattern.children[0].children

        for index, cmd in enumerate(pattern):
            if isinstance(cmd, docopt_lite.Command):
                subcmd = parent_cmd[cmd.name]
                parent_cmd = subcmd
            else:
                break

        #The last command node (leaf) will need this pattern to set arguments to parser
        cmd.parameters = pattern[index:]

        return parent_cmd

if __name__ == "__main__":
    clif = CLIF("clif", ["test/cmds", "test/cmds/subcmds"])

