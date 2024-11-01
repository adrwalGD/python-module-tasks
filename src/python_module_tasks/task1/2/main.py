def main():
    print("Enter numbers separated by space: ")
    in_str = input()
    numbers = [int(x) for x in in_str.split()]
    numbers = tuple(set(numbers))
    print(numbers)
    print(min(numbers), max(numbers))


if __name__ == "__main__":
    main()
