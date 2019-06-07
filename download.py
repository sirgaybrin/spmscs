import  argparse
parser = argparse.ArguementParser()
parser.add_argument("list",  action="store_true")
args = parser.parse_args()
if args.list:
    password = input
