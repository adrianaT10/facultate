import sys

import check

FILENAMES = [
    'tests/sample.in',
    'tests/test1.in',
    'tests/test2.in',
    'tests/test3.in',
    'tests/test4.in',
    ]
SCORES = [
    10,
    625,
    595,
    710,
    950,
    ]

def main(argv):
    verbose = False
    if len(argv) > 1:
        if argv[1] == '-v':
            verbose = True
        else:
            print('Unknown arguments')
    check.test_all(FILENAMES, SCORES, verbose=verbose)

if __name__ == '__main__':
    main(sys.argv)


