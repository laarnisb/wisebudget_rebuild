def generate_recommendation(category, amount):
    if category == "Wants" and amount > 200:
        return "Consider reducing discretionary expenses."
    elif category == "Needs" and amount > 1000:
        return "Review essential expenses for possible savings."
    elif category == "Savings" and amount < 100:
        return "Try to increase your savings to improve financial health."
    return "Your spending in this category is within reasonable limits."
