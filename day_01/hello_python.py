"""Day 01: Practice print(), variables, input(), and f-strings."""


def main():
    print("Hello, Python!")
    name = input("Apna naam likho: ").strip() or "Learner"
    language = "Python"
    day = 1
    print(f"Welcome, {name}!")
    print(f"Aaj meri {language} practice ka day {day} hai.")


if __name__ == "__main__":
    main()
