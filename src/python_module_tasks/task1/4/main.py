import pprint


def main():
    inp = input("Give me a string: ")
    chars_dict = {}
    for char in inp:
        chars_dict[char] = chars_dict.get(char, 0) + 1

    pprint.pprint(chars_dict)


if __name__ == "__main__":
    main()
