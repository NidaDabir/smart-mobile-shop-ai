def chatbot_reply(msg):

    msg = msg.lower()

    if "hello" in msg:
        return "Hello! Welcome to Mobile Shop"

    elif "price" in msg:
        return "We have mobiles from 5000 to 150000"

    elif "best phone" in msg:
        return "Best phones: iPhone 15, Galaxy S23, OnePlus 11"

    elif "cheap" in msg:
        return "Redmi and Realme are best budget phones"

    elif "apple" in msg:
        return "Best Apple phone: iPhone 15"

    elif "samsung" in msg:
        return "Best Samsung phone: Galaxy S23"

    elif "budget" in msg:
        return "Best budget phone: Redmi Note 12"

    elif "camera" in msg:
        return "Best camera phone: Pixel 7"

    elif "battery" in msg:
        return "Best battery phone: Samsung M34"

    else:
        return "Ask about Apple, Samsung, Camera, Battery or Budget"
