""" modules for all our regular expression variables """
from django.core.validators import RegexValidator


# REGEX

# Nigeria valid number check
PHONE_REGEX = RegexValidator(regex=r'^0[789]\d{9}$',
                             message=("Enter a \
        valid Nigerian phone number pattern that starts with '0' and 2nd \
            number either starts with 8, 7, or 9 with additional 9 numbers."))


SCORE_REGEX = RegexValidator(regex=r'^[0-9]+$',
                             message=(" Enter a \
        valid value of at least 2 attached numbers say 70, 65, 100. The \
        percent symbol (%) will be attached to your input automatically."))

NAME_REGEX = RegexValidator(regex=r'^[a-zA-Z\s]+$',
                            message=(
                                "Enter a valid name and it must be in either lowercase or uppercase\
                        alphabets. Digits, underscores etc., are not allowed."))

ALPHA_NUMERICS = RegexValidator(regex=r'^[A-Za-z0-9_-\s]*$',
                                message=(
                                    "Enter a valid digits and or letters it must be \
                in either lowercase or uppercase alphabets.")
                                )

# from stackoverflow -> http://regexr.com/?346hf (test it here)
DATE_REGEX = RegexValidator(
    regex=r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$',
    message=("Enter a valid value that consist of number and a slash\
                in standard date time format eg. 1/5/2024 (DD/MM/YYYY) or ( DD-MM-YYYY).")
)


TIME_REGEX = RegexValidator(
    regex=r'^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$',
    message=("Enter a valid value that consist of number from 0-9 with \
                                a colon (:) in between the two numbers.")
)