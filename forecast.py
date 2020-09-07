"""
Fetch humidity forecast data.
"""

import click
import matplotlib.dates as md
import matplotlib.pyplot as plt

from src import datafetch


@click.group()
def cli():
    pass


@cli.command()
@click.argument("location")
@click.argument("apikey")
@click.option("--output", "-o", type=click.File("w"),
              default="forecast.png",
              help="File to save the plot into.")
def forecast(location, apikey, output):
    """
    Get humidity forecast for the given location.

    The data is fetched from OpenWeather, so an OpenWeather API key with access
    to 3 hour forecast must be given. The location can be just a city (e.g.
    "Helsinki"), or include a country code (e.g. "Helsinki,FI").
    """
    humidity_dict = datafetch.humidity_forecast(location, apikey)

    humidity_tuples = sorted(humidity_dict.items())
    t, hum = zip(*humidity_tuples)

    plt.figure(figsize=(10, 6))
    plt.plot(t, hum)

    plt.title(location)
    plt.ylim(40, 100)
    plt.xlim(min(t), max(t))
    plt.ylabel("Humidity (%)")
    plt.xlabel("Date and time")
    ax = plt.gca()
    ax.xaxis.grid(True, which='minor', color="k", alpha=0.3, linestyle="--")
    ax.xaxis.grid(True, which='major', color="k", alpha=1.0, linestyle="-")
    ax.yaxis.grid(True, which="major")
    ax.xaxis.set_major_formatter(md.DateFormatter("%d.%m."))
    ax.xaxis.set_major_locator(md.DayLocator())
    ax.xaxis.set_minor_locator(md.HourLocator(byhour=range(0, 24, 3)))
    ax.xaxis.set_minor_formatter(md.DateFormatter("%H"))
    ax.xaxis.set_tick_params(which='major', pad=15)

    plt.tight_layout()
    plt.savefig(output)


if __name__ == "__main__":
    cli()
