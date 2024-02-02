import argparse
import utils


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l",
    "--list-probs",
    action="store_true",
    help="show current probabilities of each student to be chosen and exit",
)
args, remaining = parser.parse_known_args()
if args.list_probs:
    print(utils.list_probs())
    parser.exit(0)

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser],
)
parser.add_argument(
    "-d",
    "--draw",
    type=int,
    help="draw a number of number_of_student(int) number of people",
    default=-1,
)
parser.add_argument(
    "-a",
    "--absent",
    type=str,
    help="filter people in this draw, use `,` to separate them. The probability of filtered people will increase after this draw is over",
)

parser.add_argument(
    "-n",
    "--new-data",
    type=str,
    help="Reset data, use `,` to separate personnel tags. Meanwhile, the old data is saved in `<data_csv_filepath>.bak`",
)

parser.add_argument(
    "-i",
    "--import-data",
    type=str,
    help="Import data, `*` separates several states of participation on the left, and several states of leave on the right. Each state is separated by `,`, and the key-value pair is `name:count`",
)

args, remaining = parser.parse_known_args(remaining)
if args.draw > -1:
    if args.absent is not None:
        ab = args.absent.split(",")
    else:
        ab = []
    print(utils.draw(args.draw, ab))
    parser.exit(0)

if args.new_data is not None:
    ab = args.new_data.split(",")
    if len(ab) == 1 and ab[0] == "":
        ab = []

    utils.new_data(ab)
    parser.exit(0)

if args.import_data is not None:
    res = args.import_data.split("*")
    # print(res)
    sele_dict = dict()
    abs_dict = dict()

    if res[0] != "":
        items = res[0].split(",")
        for item in items:
            arr = item.split(":")
            sele_dict[arr[0].strip()] = int(arr[1].strip())
    if res[1] != "":
        items = res[-1].split(",")
        for item in items:
            arr = item.split(":")
            abs_dict[arr[0].strip()] = int(arr[1].strip())

    utils.import_data(sele_dict, abs_dict)
