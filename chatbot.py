def chatbot_response(user_input):

    user_input = user_input.lower()

    if "samsung" in user_input:
        return "Best Samsung phones: Galaxy S21 FE, Galaxy S23"

    elif "apple" in user_input:
        return "Best iPhones: iPhone 13, iPhone 14, iPhone 15"

    elif "under 50000" in user_input:
        return "Best phones under 50000: OnePlus 11R, Galaxy S21 FE"

    elif "best phone" in user_input:
        return "Best phones: iPhone 15, Galaxy S23, OnePlus 11"

    else:
        return "Please ask about Samsung, Apple, OnePlus, budget, etc."
