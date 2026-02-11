from django.core.exceptions import ValidationError

class PasswordComplexityValidator:
    def validate(self, password, user=None):
        errors = []
        if len(password) < 8:
            errors.append("Password must contain at least eight characters.")

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

        if not has_upper:
            errors.append("Password must contain at least one upper character.")
        if not has_lower:
            errors.append("Password must contain at least one lower character.")
        if not has_digit:
            errors.append("Password must contain at least one digit.")
        if not has_special:
            errors.append("Password must contain at least one special character.")

        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        return (
            "Your password must contain at least 8 characters, including "
            "uppercase, lowercase, digits, and special characters."
        )