import sys


def get_extension(file_name):
    if "." not in file_name:
        raise ValueError("No extension found")
    return file_name.split(".")[-1]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_name>")
        sys.exit(1)
    file_name = sys.argv[1]
    try:
        print(get_extension(file_name))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
