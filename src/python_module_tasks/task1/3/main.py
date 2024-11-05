import os
import pprint
import re
import sys


def read_acces_log(file_path: str) -> list[str]:
    with open(file_path, "r") as file:
        return file.readlines()


def get_user_agent(line: str) -> str:
    return re.findall(r'"([^"]+)"$', line)[0]


def main():
    file_path = input("Enter file path: ")
    if os.path.exists(file_path) is False:
        print("File not found")
        sys.exit(1)
    lines = read_acces_log(file_path)
    user_agents_dict = {}
    for line in lines:
        user_agent = get_user_agent(line)
        user_agents_dict[user_agent] = user_agents_dict.get(user_agent, 0) + 1

    print("Different user agents: ", len(user_agents_dict))
    print("User agents requests count: ")
    pprint.pprint(user_agents_dict)


if __name__ == "__main__":
    main()
