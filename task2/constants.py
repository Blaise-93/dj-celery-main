""" a module that helps us to collate all the choices for our pharmcare_patient_details
    tables as well as validate some form field characters inputted by the user.
    For example `gender_choices` - helps us check and prepopulate if the patient
    is a male or a female. So, it is left for a pharmacists to fill in the field for the
    said patient.
    """


from django.core.validators import RegexValidator


GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),

    )

UNIT_CHOICES = (
    ("in_cm", "in centimeters"),
    ("in_inch", "in inches"),
    ("in_foot", "in feet"),
    ("in_meter", "in meters"),
)

MARITAL_STATUS = (
        ("Married", "Married"),
        ("Single", "Single"),
        ("Married with Kids", "Married with Kids"),
        ("Married without Kids", "Married without Kids"),
        ("Divorced", "Divorced"),
        ("Single Parent", "Single Parent"),
        ("Other", "Other"),

    )

PATIENT_STATE = (
        ("Adult", "Adult"),
        ("Child", "Child"),
        ("Toddler", "Toddler"),
        ("Adolescent", "Adolescent"),
        ("Elderly", "Elderly")

    )

PRORITY_CHOICES = (
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    )

# REGEX 

# Nigeria valid number check
PHONE_REGEX = RegexValidator(regex=r'^0[789]\d{9}$',
                             message=("Enter a \
        valid Nigerian phone number pattern that starts with '0' and 2nd \
            number either starts with 8, 7, or 9 with additional 9 numbers."))


SCORE_REGEX  = RegexValidator(regex=r'^[0-9]+$',
                             message=(" Enter a \
        valid value of at least 2 attached numbers say 70, 65, 100. The \
        percent symbol (%) will be attached to your input automatically."))

NAME_REGEX = RegexValidator(regex=r'^[a-zA-Z\s]+$',
                            message=(
                "Enter a valid name and it must be in either lowercase or uppercase\
                        alphabets. Digits, underscores etc., are not allowed."))

ALPHA_NUMERICS = RegexValidator(regex=r'^[A-Za-z0-9_-\s]*$',
                                          message=(
                "Enter a valid digits and or letters it must be in either lowercase or uppercase\
                        alphabets."))