import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def calculate_collection_priority(fill_level, waste_weight, days_since_collection):

    # -------------------------------------------------
    # 1. Define input variables
    # -------------------------------------------------

    fill = ctrl.Antecedent(np.arange(0, 101, 1), 'fill')
    weight = ctrl.Antecedent(np.arange(0, 101, 1), 'weight')
    days = ctrl.Antecedent(np.arange(0, 8, 1), 'days')

    priority = ctrl.Consequent(
        np.arange(0, 101, 1),
        'priority'
    )

    # -------------------------------------------------
    # 2. Membership functions
    # -------------------------------------------------

    # Fill level
    fill['low'] = fuzz.trimf(
        fill.universe,
        [0, 0, 40]
    )

    fill['medium'] = fuzz.trimf(
        fill.universe,
        [20, 50, 80]
    )

    fill['high'] = fuzz.trimf(
        fill.universe,
        [60, 100, 100]
    )

    # Waste weight
    weight['low'] = fuzz.trimf(
        weight.universe,
        [0, 0, 30]
    )

    weight['medium'] = fuzz.trimf(
        weight.universe,
        [15, 40, 65]
    )

    weight['high'] = fuzz.trimf(
        weight.universe,
        [50, 100, 100]
    )

    # Days since collection
    days['recent'] = fuzz.trimf(
        days.universe,
        [0, 0, 2]
    )

    days['moderate'] = fuzz.trimf(
        days.universe,
        [1, 3, 5]
    )

    days['long'] = fuzz.trimf(
        days.universe,
        [4, 7, 7]
    )

    # Collection priority
    priority['low'] = fuzz.trimf(
        priority.universe,
        [0, 0, 40]
    )

    priority['medium'] = fuzz.trimf(
        priority.universe,
        [25, 50, 75]
    )

    priority['high'] = fuzz.trimf(
        priority.universe,
        [60, 100, 100]
    )

    # -------------------------------------------------
    # 3. Fuzzy Rules
    # -------------------------------------------------

    rule1 = ctrl.Rule(
        fill['low'] & weight['low'] & days['recent'],
        priority['low']
    )

    rule2 = ctrl.Rule(
        fill['medium'] & weight['medium'],
        priority['medium']
    )

    rule3 = ctrl.Rule(
        fill['high'],
        priority['high']
    )

    rule4 = ctrl.Rule(
        fill['high'] & weight['high'],
        priority['high']
    )

    rule5 = ctrl.Rule(
        fill['high'] & days['long'],
        priority['high']
    )

    rule6 = ctrl.Rule(
        weight['high'] & days['long'],
        priority['high']
    )

    rule7 = ctrl.Rule(
        fill['medium'] & days['long'],
        priority['high']
    )

    rule8 = ctrl.Rule(
        fill['low'] & weight['medium'] & days['long'],
        priority['medium']
    )

    # -------------------------------------------------
    # 4. Create control system
    # -------------------------------------------------

    priority_control = ctrl.ControlSystem([
        rule1,
        rule2,
        rule3,
        rule4,
        rule5,
        rule6,
        rule7,
        rule8
    ])

    simulation = ctrl.ControlSystemSimulation(
        priority_control
    )

    # -------------------------------------------------
    # 5. Give inputs
    # -------------------------------------------------

    # Keep values within valid ranges
    fill_level = max(0, min(100, fill_level))
    waste_weight = max(0, min(100, waste_weight))
    days_since_collection = max(
        0,
        min(7, days_since_collection)
    )

    simulation.input['fill'] = fill_level
    simulation.input['weight'] = waste_weight
    simulation.input['days'] = days_since_collection

    # -------------------------------------------------
    # 6. Defuzzification
    # -------------------------------------------------

    simulation.compute()

    result = simulation.output['priority']

    # -------------------------------------------------
    # 7. Convert numerical result into status
    # -------------------------------------------------

    if result < 40:
        status = "LOW PRIORITY"

    elif result < 70:
        status = "MEDIUM PRIORITY"

    else:
        status = "HIGH PRIORITY"

    return result, status