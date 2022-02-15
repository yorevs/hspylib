import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='PROG')
    subparsers = parser.add_subparsers(help='sub-command help')

    # create the parser for the "a" command
    parser_a = subparsers.add_parser('a', help='a help')
    parser_a.add_argument("--opt1", action='store_true')
    parser_a.add_argument("--opt2", action='store_true')

    # create the parser for the "b" command
    parser_b = subparsers.add_parser('b', help='b help')
    parser_b.add_argument("--opt3", action='store_true')
    parser_b.add_argument("--opt4", action='store_true')

    # parse some argument lists
    print(parser.parse_args())
