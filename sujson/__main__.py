from argparse import ArgumentParser
import logging
import os

from . import __version__
from ._errors import SujsonError
from ._sujson import Sujson
from ._logger import setup_custom_logger

logger = setup_custom_logger("sujson")


parser = ArgumentParser(description="%(prog)s v{}".format(__version__))
parser.add_argument(
    "-f", "--force", action="store_true", help="Force overwrite existing files"
)
parser.add_argument("-d", "--debug", action="store_true", help="Print debugging output")
parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose output")
parser.add_argument(
    "-n",
    "--dry-run",
    action="store_true",
    help="Do not run, only print what would be done",
)
parser.add_argument(
    "--version",
    action="version",
    version="%(prog)s v{}".format(__version__),
    help="Print version and exit",
)
subparsers = parser.add_subparsers(dest="subcommand")


def argument(*name_or_flags, **kwargs):
    """Convenience function to properly format arguments to pass to the
    subcommand decorator.
    """
    return (list(name_or_flags), kwargs)


# https://gist.github.com/mivade/384c2c41c3a29c637cb6c603d4197f9f
def subcommand(args=[], parent=subparsers):
    """Decorator to define a new subcommand in a sanity-preserving way.
    The function will be stored in the ``func`` variable when the parser
    parses arguments so that it can be called directly like so::
        args = parser.parse_args()
        args.func(args)
    Usage example::
        @subcommand([argument("-d", help="Enable debug mode", action="store_true")])
        def subcommand(args):
            print(args)
    Then on the command line::
        $ python parser.py subcommand -d
    """

    def decorator(func):
        parser = parent.add_parser(func.__name__, description=func.__doc__)
        for arg in args:
            parser.add_argument(*arg[0], **arg[1])
        parser.set_defaults(func=func)

    return decorator


@subcommand(
    [
        argument(
            "input", type=str, help="Input file, currently only .xslx or .csv supported"
        ),
        argument("-c", "--config", type=str, help="Config file"),
        argument(
            "-o",
            "--output",
            type=str,
            help="Output file, currently only .json supported. If not given, will write to STDOUT.",
        ),
    ]
)
def ingest(args):
    logger.debug("Ingesting with arguments: {}".format(args))
    sujson = Sujson(force=args.force, dry_run=args.dry_run)

    suffix = os.path.splitext(args.input)[1]
    if suffix in [".xls", ".xlsx"]:
        sujson.import_xslx(
            args.input,
            args.output,
            config_file=args.config
            # TODO: add other possible arguments here (e.g. those from config)
        )
    elif suffix in [".csv"]:
        sujson.import_csv(
            args.input,
            args.output,
            config_file=args.config
            # TODO: add other possible arguments here (e.g. record separator)
        )
    else:
        raise SujsonError("Unknown input file suffix {}".format(suffix))


@subcommand(
    [
        argument("input", type=str, help="Input suJSON file"),
        argument(
            "-o",
            "--output",
            type=str,
            help="Output file, currently only .pickle supported.",
        ),
    ]
)
def export(_args):
    """
    Reads subjective data from a suJSON file and stores the data in a file format of choice
    """
    logger.debug("Ingesting with arguments: {}".format(_args))
    sujson = Sujson(force=_args.force, dry_run=_args.dry_run)

    suffix = os.path.splitext(_args.input)[1]
    output_suffix = os.path.splitext(_args.output)[1]

    if suffix not in [".json"]:
        raise SujsonError("Unsupported input file suffix {}".format(suffix))

    if output_suffix not in [".pickle"]:
        raise SujsonError("Unsupported output file suffix {}".format(output_suffix))

    export_result = sujson.export(_args.input, _args.output)

    # TODO 6. Inform the user what is the status of the operation (did it go ok?)
    print(export_result)

if __name__ == "__main__":
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    elif args.verbose:
        logger.setLevel(logging.INFO)
    if args.subcommand is None:
        parser.print_help()
    else:
        args.func(args)
