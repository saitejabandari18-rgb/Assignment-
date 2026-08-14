schedule = {
    "monday": {"python", "statistics", "english"},
    "wednesday": {"python", "databases"},
    "friday": {"statistics", "python", "presentation"}
}


def days_with(schedule, course) -> set:
    result = set()

    for day in schedule:
        if course in schedule[day]:
            result.add(day)

    return result


def every_day(schedule) -> set:
    if len(schedule) == 0:
        return set()

    days = list(schedule.values())

    common_courses = days[0].copy()

    for courses in days[1:]:
        common_courses = common_courses & courses

    return common_courses


def course_count(schedule, day) -> int:
    if day not in schedule:
        return 0

    return len(schedule[day])


def busiest_days(schedule) -> list:
    if len(schedule) == 0:
        return []

    highest = 0

    for day in schedule:
        number_of_courses = len(schedule[day])

        if number_of_courses > highest:
            highest = number_of_courses

    result = []

    for day in schedule:
        if len(schedule[day]) == highest:
            result.append(day)

    return sorted(result)


# Demo
if __name__ == "__main__":
    print("Days with python:", days_with(schedule, "python"))
    print("Days with statistics:", days_with(schedule, "statistics"))
    print("Days with maths:", days_with(schedule, "maths"))

    print("Courses every day:", every_day(schedule))

    print("Courses on Monday:", course_count(schedule, "monday"))
    print("Courses on Sunday:", course_count(schedule, "sunday"))

    print("Busiest days:", busiest_days(schedule))