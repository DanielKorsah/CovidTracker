import requests
import pprint
from matplotlib import pyplot as plt
from datetime import datetime, date, timedelta

response = requests.get(
    "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.json")

data_dict = response.json()
pp = pprint.PrettyPrinter()

date_format = "%Y-%m-%d"


def get_all_data(country_code="GBR"):
    all_days = data_dict[country_code]["data"]
    country = data_dict[country_code]["location"]
    return country, all_days


def get_most_recent_total_cases_per_million_and_date(country_code="GBR"):

    cases_per_mil = None
    index = -1
    while cases_per_mil == None:
        try:
            cases_per_mil = data_dict["USA"]["data"][index]["total_cases_per_million"]
            date_of_last_total = data_dict["USA"]["data"][index]["date"]
        except KeyError:
            index -= 1
    return (cases_per_mil, date_of_last_total)


def plot_daily_cases(*country_codes, data_of_interest="new_cases"):

    if len(country_codes) > 6:
        print("Max countries in one plot is six.")
        return None

    cases_all = []
    dates_all = []

    colours = ["blue", "green", "red", "cyan", "magenta", "black"]
    colour_index = 0

    country_names = []
    plt.figure(figsize=(12, 8))

    for code in country_codes:

        cases = []
        dates = []
        country_name, all_data = get_all_data(code)
        country_names.append(country_name)

        for entry in all_data:
            try:
                cases.append(entry[data_of_interest])
            except KeyError:
                entry_date = entry["date"]
                print(
                    f"no '{data_of_interest}' value in {country_name} on {entry_date}.")
                cases.append(None)
            dates.append(datetime.strptime(entry["date"], date_format))

        cases_all.append(cases)
        dates_all.append(dates)

    for cases, dates, country in zip(dates_all, cases_all, country_names):
        plt.plot(cases, dates, label=country, color=colours[colour_index])
        colour_index += 1

    axes = plt.gca()
    axes.yaxis.grid()

    plt.xlabel("Date")
    label = data_of_interest.replace("_", " ")
    label = label.title()
    plt.ylabel(label)
    plt.legend(loc="upper left")

    filename = "_".join(country_codes)
    title = f"{label} in\n"
    title += "/".join(country_names)
    plt.title(title)

    plt.savefig(f"{filename}_{data_of_interest}.png")
    plt.show()


plot_daily_cases("GBR", "USA", "DEU", "ITA", "ESP", "FRA",

                 data_of_interest="new_deaths")
plot_daily_cases("GBR", "USA", "DEU", "ITA", "ESP", "FRA",
                 data_of_interest="new_deaths_smoothed_per_million")

plot_daily_cases("GBR", "USA", "DEU", "ITA", "ESP", "FRA",
                 data_of_interest="new_cases")

plot_daily_cases("GBR", "USA", "DEU", "ITA", "ESP", "FRA",
                 data_of_interest="new_cases_smoothed_per_million")

country, data = get_all_data("GBR")
cpm, date = get_most_recent_total_cases_per_million_and_date("GBR")
print(f"{cpm} cases per million population in {country} as of {date}.")
