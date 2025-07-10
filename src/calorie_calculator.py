def calculate_maintenance_kcal(age, sex, height, bodyweight_kg, activity_level):
    """
    Estimates daily maintenance calories using the Harris-Benedict formula.

    The result represents the estimated number of calories required to maintain
    current body weight, based on age, biological sex, height, weight, and activity level.

    Parameters:
    - age (int): Age in years.
    - sex (str): "Männlich" (male) or "Weiblich" (female).
    - height (float): Height in centimeters.
    - bodyweight_kg (float): Weight in kilograms.
    - activity_level (str): Activity level, one of:
        "Sitzend", "Leicht aktiv", "Moderat aktiv", "Sehr aktiv", "Extrem aktiv".

    Returns:
    - int: Estimated maintenance calories (kcal/day).
    """
    if sex == "Männlich":
        bmr = 10 * bodyweight_kg + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * bodyweight_kg + 6.25 * height - 5 * age - 161

    activity_factors = {
        "Sitzend": 1.2,
        "Leicht aktiv": 1.375,
        "Moderat aktiv": 1.55,
        "Sehr aktiv": 1.725,
        "Extrem aktiv": 1.9
    }

    return int(bmr * activity_factors[activity_level])