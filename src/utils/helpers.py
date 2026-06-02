def build_greeting() -> str:
    return (
        "Hello! I am SmartDesk AI, your IT and HR support "
        "assistant at Roadmap Consulting.\n\n"
        "I can help you with:\n"
        "  IT support questions (passwords, VPN, MFA, email)\n"
        "  HR policy questions (leave, WFH, reimbursement)\n"
        "  Creating support tickets for issues I cannot solve\n"
        "  Checking the status of your existing tickets\n\n"
        "How can I help you today?"
    )


def build_api_error_response(service: str = "the service") -> str:
    return (
        f"I am sorry — I am having trouble connecting to "
        f"{service} right now.\n\n"
        f"This is usually a temporary issue. "
        f"Please try again in a moment.\n\n"
        f"If the problem continues please contact IT directly "
        f"at it-support@roadmapconsulting.com or ext. 2020."
    )


def build_unclear_response() -> str:
    return (
        "I am not sure I understood that. Could you please "
        "rephrase your question?\n\n"
        "For example you could ask me:\n"
        "  'How do I reset my password?'\n"
        "  'How many leave days do I get?'\n"
        "  'What is the status of my ticket?'"
    )


def validate_message(message: str) -> dict:
    if not message or not isinstance(message, str):
        return {"valid": False, "reason": "empty", "cleaned": ""}

    cleaned = message.strip()

    if not cleaned:
        return {"valid": False, "reason": "empty", "cleaned": ""}

    if len(cleaned) < 2:
        return {"valid": False, "reason": "too_short", "cleaned": cleaned}

    if len(cleaned) > 1000:
        return {"valid": False, "reason": "too_long", "cleaned": cleaned[:1000]}

    vowels = set("aeiouAEIOU")
    words  = cleaned.split()
    if len(words) > 3:
        has_vowels = any(
            any(c in vowels for c in word)
            for word in words
        )
        if not has_vowels:
            return {"valid": False, "reason": "gibberish", "cleaned": cleaned}

    return {"valid": True, "reason": "ok", "cleaned": cleaned}


def get_validation_response(reason: str) -> str:
    responses = {
        "empty": (
            "It looks like you did not type anything.\n"
            "Please type your question and I will be happy to help!"
        ),
        "too_short": (
            "I need a bit more information to help you.\n"
            "Could you please describe what you need?"
        ),
        "too_long": (
            "Your message is quite long! I have read the "
            "first part.\n"
            "Could you summarise your question in one or "
            "two sentences so I can help you better?"
        ),
        "gibberish": (
            "I am not sure I understood that.\n\n"
            "Could you please rephrase your question?\n\n"
            "For example:\n"
            "  'How do I reset my password?'\n"
            "  'How many leave days do I get?'\n"
            "  'What is the status of my ticket?'"
        )
    }
    return responses.get(reason, build_unclear_response())


def is_greeting(message: str) -> bool:
    greetings = [
        "hi", "hello", "hey", "good morning", "good afternoon",
        "good evening", "howdy", "greetings", "sup", "hiya",
        "hi there", "hello there", "hey there"
    ]
    return message.lower().strip() in greetings


def build_greeting_response() -> str:
    return (
        "Hello! Great to hear from you.\n\n"
        "I am SmartDesk AI, your IT and HR support assistant "
        "at Roadmap Consulting.\n\n"
        "How can I help you today? You can ask me about:\n"
        "  IT support (passwords, VPN, MFA, email setup)\n"
        "  HR policies (leave, WFH, reimbursement)\n"
        "  Creating a support ticket\n"
        "  Checking the status of your existing tickets"
    )


def is_thanks(message: str) -> bool:
    thanks_words = [
        "thanks", "thank you", "thank you so much",
        "many thanks", "cheers", "appreciated",
        "that helped", "that was helpful", "great thanks",
        "ok thanks", "okay thanks"
    ]
    message_lower = message.lower().strip()
    return any(t in message_lower for t in thanks_words)


def build_thanks_response() -> str:
    return (
        "You are very welcome! I am glad I could help.\n\n"
        "Is there anything else I can assist you with today?"
    )


def ask_for_email() -> str:
    return (
        "Could you please share your work email address "
        "so I can look that up for you?"
    )


def build_ticket_summary(query: str, email: str, category: str) -> str:
    separator = "-" * 40
    return (
        f"I would like to create a support ticket for you.\n\n"
        f"Please review the details below:\n\n"
        f"{separator}\n"
        f"  📋 Title    : {query[:80]}\n"
        f"  🏷  Category : {category}\n"
        f"  📧 Email    : {email}\n"
        f"  🤖 Created by: SmartDesk AI Agent\n"
        f"{separator}\n\n"
        f"Shall I go ahead and create this ticket?\n"
        f"Type YES to confirm or NO to cancel."
    )


def categorise_query(query: str) -> str:
    hr_keywords = [
        "leave", "holiday", "vacation", "sick", "maternity",
        "paternity", "wfh", "work from home", "reimbursement",
        "salary", "payroll", "hr", "onboarding", "policy"
    ]
    query_lower = query.lower()
    for keyword in hr_keywords:
        if keyword in query_lower:
            return "HR Support"
    return "IT Support"
