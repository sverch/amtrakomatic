"""
Library to automate reading and getting to the purchase page for Amtrak tickets
"""

import sys
import click
from amtrakomatic import scrape_amtrak
from amtrakomatic import fuzzy_match

@click.command()
@click.option('--source', default=None, help='Source station.')
@click.option('--destination', default=None, help='Destination station.')
@click.option('--train-name', default=None, help='Specific train to select.')
@click.option('--date', default=None, help='Date string.')
@click.option('--csv', default=None, help='CSV with searches.')
@click.option('--interactive/--no-interactive', default=False,
              help='Whether to pause after each csv search.')
@click.option('--use-points/--no-use-points', default=False)
@click.option('--dry-run/--no-dry-run', default=False,
              help='Whether this is a dry run (print station matches).')
# pylint: disable=too-many-arguments
def amtrak_search(source, destination, train_name, date, csv, interactive, use_points, dry_run):
    """
    Can give you all results for a single search, or get you to the checkout page for a list of
    searches in a CSV.
    """
    if source and destination and date:
        source_match = fuzzy_match.station(source)
        destination_match = fuzzy_match.station(destination)
        print("\nFrom: %s (%s)\nTo: %s (%s)\n" % (
            source_match[0],
            source_match[1],
            destination_match[0],
            destination_match[1]))
        if dry_run:
            sys.exit(0)
        scrape_amtrak.get_all_fares(source, destination, date, use_points).pretty_print(train_name)
    elif csv:
        scrape_amtrak.iterate_csv_trips(csv, interactive)
    else:
        click.echo('Expected source, destination, and date to all be set, or csv to be set.')

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    amtrak_search()
