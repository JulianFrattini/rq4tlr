from util.uc import UseCase

from parser.loader import parse_dataset
from parser.etoursparser import EtoursParser

def main():
    parser = EtoursParser()
    usecases: list[UseCase] = parse_dataset('eTour', parser)
    print(usecases)


if __name__ == "__main__":
    main()