import sys


def get_extension(file_name):
    if "." not in file_name:
        raise ValueError("No extension found")
    return file_name.split(".")[-1]


if __name__ == "__main__":
    file_name = sys.argv[1]
    print(get_extension(file_name))
