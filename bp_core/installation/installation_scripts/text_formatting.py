class BColors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_green(*args):
    print(BColors.OKGREEN + " ".join(map(str, args)) + BColors.ENDC)


def print_red(*args):
    print(BColors.FAIL + " ".join(map(str, args)) + BColors.ENDC)


def print_cyan(*args):
    print(BColors.OKCYAN + " ".join(map(str, args)) + BColors.ENDC)
