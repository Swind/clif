from sh import cat

def cat_sys_info_cmd(**kwargs):
    """
    Usage:
        cat sys info --cpu --memory --repeat <repeat>

    Options:
        -c,--cpu               Show CPU information
        -m,--memory            Show memory usage
        -r,--repeat <repeat>   Repeat time [default: 1]
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

