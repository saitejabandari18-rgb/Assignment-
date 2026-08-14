def parse_log(data: str) -> list:
    log = []

    entries = data.split(",")

    for entry in entries:
        city, temperature = entry.split(":")

        city = city.strip()
        temperature = float(temperature.strip())

        log.append((city, temperature))

    return log


def average_temp(log, city) -> float:
    temperatures = []

    for item_city, temperature in log:
        if item_city == city:
            temperatures.append(temperature)

    if len(temperatures) == 0:
        return 0.0

    average = sum(temperatures) / len(temperatures)

    return round(average, 1)


def hottest_city(log) -> str:
    cities = set()

    for city, temperature in log:
        cities.add(city)

    hottest = ""
    highest_average = -1

    for city in cities:
        average = average_temp(log, city)

        if average > highest_average:
            highest_average = average
            hottest = city

    return hottest


def measurement_counts(log) -> dict:
    counts = {}

    for city, temperature in log:
        if city in counts:
            counts[city] += 1
        else:
            counts[city] = 1

    return counts


# Demo
if __name__ == "__main__":
    data = (
        "berlin:21.5, hamburg:18.0, berlin:24.0, munich:26.5, "
        "hamburg:17.5, berlin:19.0, munich:30.0"
    )

    log = parse_log(data)

    print("Parsed log:", log)
    print("Berlin average:", average_temp(log, "berlin"))
    print("Hamburg average:", average_temp(log, "hamburg"))
    print("Munich average:", average_temp(log, "munich"))
    print("Unknown city:", average_temp(log, "london"))
    print("Hottest city:", hottest_city(log))
    print("Measurement counts:", measurement_counts(log))