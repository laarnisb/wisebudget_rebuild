def categorize_transaction(description):
    wants_keywords = ["restaurant", "entertainment", "shopping"]
    needs_keywords = ["rent", "utilities", "groceries"]
    savings_keywords = ["transfer", "investment", "savings"]

    desc = description.lower()
    if any(word in desc for word in wants_keywords):
        return "Wants"
    elif any(word in desc for word in needs_keywords):
        return "Needs"
    elif any(word in desc for word in savings_keywords):
        return "Savings"
    else:
        return "Uncategorized"
