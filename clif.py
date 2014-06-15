import sys
import pkgutil

import logging
logger = logging.getLogger(__name__)

import inspect

import docopt_lite

def load_all_modules_from_dir(dirname):
    modules = []

    for importer, package_name, _ in pkgutil.iter_modules([dirname]):
        if package_name not in sys.modules:
            module = importer.find_module(package_name).load_module(package_name)
            modules.append(module)

    return modules

class CLIF(object):

    def __init__(self, cmd_folders, cmd_suffix = "_cmd"):
        if type(cmd_folders) is str:
            self.folders = [cmd_folders]
        else:
            self.folders = cmd_folders

        self.cmd_suffix = cmd_suffix

    def load_modules(self):
        modules_list = map(lambda folder: load_all_modules_from_dir(folder), self.folders)

        def flat_list(result, items):
            result.extend(items)
            return result

        modules = reduce(flat_list, modules_list, [])

        return modules

    def get_cmd_funcs(self, cmd_modules):

        #Return all function or class in the module and the suffix of name is <cmd_suffix>
        def find_cmd_funcs(funcs, cmd_module):
            cmd_funcs = [cmd_func for (cmd_name, cmd_func) in inspect.getmembers(cmd_module) if cmd_name.endswith(self.cmd_suffix)]
            funcs.extend(cmd_funcs)
            return funcs

        return reduce(find_cmd_funcs, cmd_modules, [])

    def load_cmds(self):
        cmd_modules = self.load_modules()
        cmd_funcs = self.get_cmd_funcs(cmd_modules)

        for cmd_func in cmd_funcs:
            logger.debug("Find command function or class %s" % cmd_func.__name__)

            if inspect.isclass(cmd_func):
                #If the command if a class, create a command class instance
                cmd_func = cmd_func()

            #Get doc string in the command
            doc = inspect.getdoc(cmd_func)

            pattern = docopt_lite.build_docopt_pattern(doc)

            print pattern

if __name__ == "__main__":
    clif = CLIF(["test/cmds", "test/cmds/subcmds"])

    clif.load_cmds()
