from util.uc import UseCase

from parser.loader import parse_dataset
from parser.etoursparser import EtoursParser

from preprocessor.processor import Preprocessor 

def main():
    parser = EtoursParser()
    usecases: list[UseCase] = parse_dataset('eTour', parser)

    preprocessor = Preprocessor()
    processed = preprocessor.pos_tagging(usecases[0].steps[0])
    print(processed)

if __name__ == "__main__":
    main()