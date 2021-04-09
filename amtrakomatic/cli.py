"""
Library to automate reading and getting to the purchase page for Amtrak tickets
"""

import click
from amtrakomatic import scrape_amtrak

@click.command()
@click.option('--source', default=None, help='Source station.')
@click.option('--destination', default=None, help='Destination station.')
@click.option('--date', default=None, help='Date string.')
@click.option('--csv', default=None, help='CSV with searches.')
@click.option('--interactive/--no-interactive', default=False,
              help='Whether to pause after each csv search.')
@click.option('--use-points/--no-use-points', default=False)
# pylint: disable=too-many-arguments
def amtrak_search(source, destination, date, csv, interactive, use_points):
    """
    Can give you all results for a single search, or get you to the checkout page for a list of
    searches in a CSV.
    """
    if source and destination and date:
        scrape_amtrak.get_all_fares(source, destination, date, use_points).pretty_print()
    elif csv:
        scrape_amtrak.iterate_csv_trips(csv, interactive)
    else:
        click.echo('Expected source, destination, and date to all be set, or csv to be set.')

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    amtrak_search()
