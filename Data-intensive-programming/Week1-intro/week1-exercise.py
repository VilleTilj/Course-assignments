from functools import reduce


# Task 1.
def mySum(x, y) -> float:
    return x + y


# Task 2.
def pascal(row: int, column: int) -> int:
    if column in (0, row):
        return 1
    return pascal(row - 1, column - 1) + pascal(row - 1, column)


# Task 3.
def balance(chars: list) -> bool:
    pass


# Task 4.
def sum_of_squares(integer_array: list) -> list:
    squares: list = list(map(lambda x: x ** 2, integer_array))
    sum_of_squares = abs(reduce(lambda x, y: x - y, squares, sum(integer_array) ** 2 / len(integer_array)))
    return sum_of_squares


# Task 6.
def sqrt(x, estimate=1.0):
    estimate = (estimate + x / estimate) / 2
    difference = abs(x - estimate ** 2)
    if difference > 0.001:
        estimate = sqrt(x, estimate)
    return estimate


def main():
    # Task 1.
    s: float = mySum(20, 21)
    print(f'Test task 1:\n  Test passed: {s == 41}\n  Expected 41 got {s}\n')

    # Task 2.
    print('Pascals triangle below:')
    for row in range(10):
        for column in range(row + 1):
            print(pascal(row, column), end=' ', flush=True)
        print()
    print()

    # Task 3.
    test3 = (balance(['(', 'a', '(', ')']))
    print(f'Test task 3:\n  Test passed: {test3 == True}\n')

    # Task 4.
    a = [1, 2, 3, 4, 5, 6]
    print(f'Test task 4:\n  Test passed: {sum_of_squares(a) == 17.5}\n   Expected 17.5 got {sum_of_squares(a)}\n')

    # Task 5.
    print('Task 5. Explaining the code snippet Scala:\n'
          '"sheena is a punk rocker she is a punk punk".split(" ").map(s => (s, 1)).groupBy(p => p._1).mapValues(v => '
          'v.length)\n')
    print('.split(" ") splits the string from the space and creates a list from the sentence.')
    print('.map creates new map collection with "tuple" value (list_element, 1)')
    print('.groupBy method groups the values / letters in the map')
    print('.mapValues creates map with the same keys but trasforms keys values using the v.lenght function.')
    print('Finally it prints a Map with the chars in alphabetical order and the letter being the key. Values are the '
          'count of how many times the char appears in the string.')

    print('Python snippet:')
    from itertools import groupby  # itertools.groupby requires the list to be sorted
    result = {r: len(s) for r, s in {p: list(v) for p, v in groupby(sorted(list(map(lambda x: (x, 1),
                                                                                    "sheena is a punk rocker she is a punk punk".split(
                                                                                        " "))),
                                                                           key=lambda x: x[0]),
                                                                    lambda x: x[0])}.items()}
    print('It does the same thing but first it creates the dict (Map) with for loops and groups and sorts it. After '
          'that it makes a list of a map using lambda and using the splitted string as the lambda attribute.')
    print(result)

    print(
        '\nSecond snippet Scala:\n"sheena is a punk rocker she is a punk punk".split(" ").map((_, 1)).groupBy(_._1).mapValues(v => v.map(_._2).reduce(_+_))')

    print('Python snippet 2:')
    result_2 = {r: reduce(lambda x, y: x + y, list(map(lambda x: x[1], s))) for r, s in {p: list(v) for p, v in groupby(
        sorted(list(map(lambda x: (x, 1), "sheena is a punk rocker she is a punk punk".split(" "))),
               key=lambda x: x[0]), lambda x: x[0])}.items()}
    print(result_2)

    # Task 6.
    print(sqrt(2))
    print(sqrt(100))
    print(sqrt(1e-16))
    print(sqrt(1e60))


if __name__ == '__main__':
    main()
