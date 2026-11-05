def detect_priority(complaint):
    complaint = complaint.lower()

    # High Priority Words

    high_words = [
        "emergency",
        "danger",
        "fire",
        "electric shock",
        "shock",
        "no electricity",
        "server down",
        "internet down",
        "security",
        "accident",
        "unsafe"
    ]

    # Medium Priority Words

    medium_words = [
        "fan",
        "light",
        "computer",
        "network",
        "wifi",
        "water",
        "projector",
        "camera",
        "printer",
        "lab",
        "classroom"
    ]

    # Check High Priority

    for word in high_words:
        if word in complaint:
            return "High"

    # Check Medium Priority

    for word in medium_words:
        if word in complaint:
            return "Medium"

    # If no important word is found

    return "Low"