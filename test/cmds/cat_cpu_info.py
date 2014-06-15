from sh import cat

def cat_sys_info_cmd(**kwargs):
    """
    Usage:
        cat sys info --cpu --memory --repeat <repeat>

    Options:
        --cpu               Show CPU information
        --memory            Show memory usage
        --repeat <repeat>   Repeat time
    """
    result = ""

    if "--cpu" in kwargs and kwargs["--cpu"]:
        print "CPU:"
        print cat("/proc/cpuinfo")

    if "--memory" in kwargs and kwargs["--memory"]:
        print "Memory:"
        print cat("/proc/meminfo")

if __name__ == "__main__":
    cat_sys_info(**{"--cpu":True, "--memory":False })

