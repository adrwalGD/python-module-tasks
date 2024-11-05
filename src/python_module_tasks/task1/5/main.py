import argparse
import os
import platform
import pprint
import socket
import sys

import cpuinfo
import psutil


def get_distro_info():
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
    }


def get_memory_info():
    memory = psutil.virtual_memory()
    return {
        "total": memory.total,
        "used": memory.used,
        "free": memory.free,
    }


def get_cpu_info():
    cpu = psutil.cpu_freq()
    cpu_info = cpuinfo.get_cpu_info()
    return {
        "model": cpu_info["brank_raw"],
        "cores": psutil.cpu_count(logical=False),
        "speed": cpu_info["hz_actual_friendly"],
    }


def get_user_info():
    return {
        "user": os.getlogin(),
    }


def get_load_average():
    return {
        "load_average": os.getloadavg(),
    }


def get_ip_address():
    return {
        "ip_address": socket.gethostbyname(socket.gethostname()),
    }


def main():
    parser = argparse.ArgumentParser(description="Get system information")
    parser.add_argument(
        "-d", "--distro", action="store_true", help="Get distro information"
    )
    parser.add_argument(
        "-m", "--memory", action="store_true", help="Get memory information"
    )
    parser.add_argument("-c", "--cpu", action="store_true", help="Get CPU information")
    parser.add_argument(
        "-u", "--user", action="store_true", help="Get user information"
    )
    parser.add_argument("-l", "--load", action="store_true", help="Get load average")
    parser.add_argument(
        "-i", "--ip", action="store_true", help="Get private IP address"
    )
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.distro:
        pprint.pprint(get_distro_info())

    if args.memory:
        pprint.pprint(get_memory_info())

    if args.cpu:
        pprint.pprint(get_cpu_info())

    if args.user:
        pprint.pprint(get_user_info())

    if args.load:
        pprint.pprint(get_load_average())

    if args.ip:
        pprint.pprint(get_ip_address())


if __name__ == "__main__":
    main()
