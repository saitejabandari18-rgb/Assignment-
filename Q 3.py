def workout_summary(name, weight_kg, *exercises, intensity=1.0, **details):
    if intensity <= 0:
        print("Error: intensity must be greater than 0.")
        return

    print("Workout report for", name)
    print("Weight:", weight_kg, "kg")
    print("Intensity:", intensity)

    total_calories = 0

    for exercise, minutes in exercises:
        calories = minutes * 5 * intensity * (weight_kg / 70)

        print(exercise, "-", round(calories), "calories")

        total_calories += calories

    if len(details) > 0:
        print("Session information:")

        for key in details:
            print(key + ":", details[key])

    total_calories = round(total_calories)

    print("Total calories:", total_calories)

    return total_calories


# Demo
if __name__ == "__main__":

    print("----- Simple workout -----")
    result = workout_summary(
        "Alex",
        70,
        ("Running", 30)
    )
    print("Returned:", result)

    print("\n----- Higher intensity -----")
    result = workout_summary(
        "Alex",
        70,
        ("Cycling", 40),
        intensity=1.5
    )
    print("Returned:", result)

    print("\n----- Workout with details
