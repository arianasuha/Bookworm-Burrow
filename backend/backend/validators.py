from django.core.exceptions import ValidationError

class PasswordComplexityValidator:
    def password_complexity_checker(password):
        errors = []
        if len(password) < 8:
            errors.append("Password must contains atleast eight characters.")
        has_lower = False
        has_upper = False
        has_digit = False
        has_special = False
        for char in password:
            ascii_val = ord(char)

            if 65 <= ascii_val <= 90:
                has_upper = True
            elif 97 <= ascii_val <= 122:
                has_lower = True
            elif 48 <= ascii_val <= 57:
                has_digit = True
            elif 33 <= ascii_val <= 47 or 58 <= ascii_val <= 64 or 91 <= ascii_val <= 96 or 123 <= ascii_val <= 127:
                has_special = True

        if has_upper == False:
            errors.append("Password must contains atleat one upper character")
        if has_lower == False:
            errors.append("Password must contains atleat one lower character")
        if has_digit == False:
            errors.append("Password must contains atleat one digit")
        if has_special == False:
            errors.append("Password must contains atleat one special character")


        if len(errors) != 0:
            raise ValidationError('\n'.join(errors))

        return True
