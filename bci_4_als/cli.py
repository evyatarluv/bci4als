"""Console script for bci_4_als."""
import sys
import click


@click.command()
@click.option('--mode',
              help='Choose which mode to run')
def main(mode):
    """Console script for bci_4_als."""

    click.echo("Hello and welcome to BCI-4-ALS")
    click.echo(mode)
    return 0


if __name__ == "__main__":
    main()
