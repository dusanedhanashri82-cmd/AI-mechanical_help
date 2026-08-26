# ============================================================
# AI SMART MECHANICAL HELP CENTER
# BACKEND - CONTACT SUPPORT
# ============================================================

# ------------------------------------------------------------
# SUPPORT TYPES
# ------------------------------------------------------------

SUPPORT_TYPES = {
    "1": "Vehicle Diagnosis",
    "2": "Technical Support",
    "3": "Service Booking",
    "4": "Roadside Assistance",
    "5": "General Inquiry"
}


# ------------------------------------------------------------
# CUSTOMER SUPPORT DETAILS
# ------------------------------------------------------------

CUSTOMER_SUPPORT = {
    "customer_care": "+91 9876543210",
    "roadside_assistance": "1800-123-4567",
    "email": "support@aimechanicalhelp.com",
    "working_hours": "Monday - Saturday (9:00 AM - 6:00 PM)"
}


# ============================================================
# FUNCTION 1
# GET SUPPORT TYPE
# ============================================================

def get_support_type(choice):
    """
    Convert support choice number into support type.
    """

    choice = str(choice)

    return SUPPORT_TYPES.get(
        choice,
        "Unknown"
    )


# ============================================================
# FUNCTION 2
# CREATE SUPPORT REQUEST
# ============================================================

def create_support_request(
    name,
    mobile,
    company,
    model,
    choice,
    message
):
    """
    Create a complete customer support request.

    Parameters:
        name    : Customer name
        mobile  : Customer mobile number
        company : Vehicle company
        model   : Vehicle model
        choice  : Support type number
        message : Customer problem

    Returns:
        Dictionary containing support request.
    """

    support = get_support_type(choice)

    request = {

        "name": name,

        "mobile": mobile,

        "company": company,

        "model": model,

        "support_type": support,

        "message": message,

        "status": "Submitted",

        "message_status":
            "Your support request has been submitted successfully!"
    }

    return request


# ============================================================
# FUNCTION 3
# VALIDATE CUSTOMER DETAILS
# ============================================================

def validate_customer_details(
    name,
    mobile,
    company,
    model
):
    """
    Validate customer and vehicle information.
    """

    errors = []

    # Name validation
    if not name or not name.strip():
        errors.append(
            "Please enter your name."
        )

    # Mobile validation
    mobile = str(mobile).strip()

    if not mobile:
        errors.append(
            "Please enter your mobile number."
        )

    elif not mobile.isdigit():
        errors.append(
            "Mobile number must contain only digits."
        )

    elif len(mobile) != 10:
        errors.append(
            "Mobile number must contain 10 digits."
        )

    # Company validation
    if not company or not company.strip():
        errors.append(
            "Please enter vehicle company."
        )

    # Model validation
    if not model or not model.strip():
        errors.append(
            "Please enter vehicle model."
        )

    return errors


# ============================================================
# FUNCTION 4
# VALIDATE PROBLEM MESSAGE
# ============================================================

def validate_message(message):

    if not message or not message.strip():

        return [
            "Please describe your problem."
        ]

    return []


# ============================================================
# FUNCTION 5
# GET CUSTOMER SUPPORT DETAILS
# ============================================================

def get_customer_support():

    return CUSTOMER_SUPPORT


# ============================================================
# FUNCTION 6
# COMPLETE SUPPORT PROCESS
# ============================================================

def submit_support_request(
    name,
    mobile,
    company,
    model,
    choice,
    message
):
    """
    Complete backend process.

    This function:
    1. Validates customer details
    2. Validates problem message
    3. Identifies support type
    4. Creates support request
    """

    # --------------------------------------------------------
    # VALIDATE CUSTOMER DETAILS
    # --------------------------------------------------------

    errors = validate_customer_details(
        name,
        mobile,
        company,
        model
    )

    # --------------------------------------------------------
    # VALIDATE MESSAGE
    # --------------------------------------------------------

    message_errors = validate_message(
        message
    )

    errors.extend(
        message_errors
    )

    # --------------------------------------------------------
    # RETURN ERROR
    # --------------------------------------------------------

    if errors:

        return {
            "success": False,
            "errors": errors,
            "request": None
        }

    # --------------------------------------------------------
    # CREATE REQUEST
    # --------------------------------------------------------

    request = create_support_request(
        name=name,
        mobile=mobile,
        company=company,
        model=model,
        choice=choice,
        message=message
    )

    # --------------------------------------------------------
    # RETURN SUCCESS
    # --------------------------------------------------------

    return {
        "success": True,
        "errors": [],
        "request": request
    }


# ============================================================
# FUNCTION 7
# GET SUPPORT MENU
# ============================================================

def get_support_menu():

    return [
        {
            "id": "1",
            "name": "Vehicle Diagnosis"
        },

        {
            "id": "2",
            "name": "Technical Support"
        },

        {
            "id": "3",
            "name": "Service Booking"
        },

        {
            "id": "4",
            "name": "Roadside Assistance"
        },

        {
            "id": "5",
            "name": "General Inquiry"
        }
    ]


# ============================================================
# FUNCTION 8
# FORMAT SUPPORT REQUEST
# ============================================================

def format_support_request(request):

    text = f"""
============================================================
📋 SUPPORT REQUEST
============================================================

👤 Name          : {request['name']}

📱 Mobile        : {request['mobile']}

🏢 Company       : {request['company']}

🚗 Vehicle Model : {request['model']}

🛠️ Support Type  : {request['support_type']}

📝 Message       : {request['message']}

📌 Status        : {request['status']}

============================================================
"""

    return text


# ============================================================
# FUNCTION 9
# FORMAT CUSTOMER SUPPORT DETAILS
# ============================================================

def format_customer_support():

    support = get_customer_support()

    text = f"""
============================================================
📞 CUSTOMER SUPPORT DETAILS
============================================================

📞 Customer Care       : {support['customer_care']}

🚑 Roadside Assistance : {support['roadside_assistance']}

📧 Email              : {support['email']}

🕒 Working Hours      : {support['working_hours']}

============================================================
"""

    return text


# ============================================================
# TEST BACKEND
# ============================================================

if __name__ == "__main__":

    print("=" * 70)

    print(
        "📞 AI SMART MECHANICAL HELP CENTER"
    )

    print(
        "📧 CONTACT SUPPORT BACKEND"
    )

    print("=" * 70)

    # --------------------------------------------------------
    # SAMPLE CUSTOMER DATA
    # --------------------------------------------------------

    name = "Test User"

    mobile = "9876543210"

    company = "Hero"

    model = "Splendor Plus"

    choice = "1"

    message = (
        "My vehicle is not starting."
    )

    # --------------------------------------------------------
    # SUBMIT REQUEST
    # --------------------------------------------------------

    result = submit_support_request(

        name=name,

        mobile=mobile,

        company=company,

        model=model,

        choice=choice,

        message=message
    )

    # --------------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------------

    if result["success"]:

        print(
            format_support_request(
                result["request"]
            )
        )

        print(
            "✅ Your support request has been "
            "submitted successfully!"
        )

        print(
            format_customer_support()
        )

        print(
            "🤖 Thank you for contacting "
            "AI Smart Mechanical Help Center."
        )

    else:

        print(
            "❌ Please correct the following:"
        )

        for error in result["errors"]:

            print(
                "•",
                error
            )