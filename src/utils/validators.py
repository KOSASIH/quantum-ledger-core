import re

class Validators:
    @staticmethod
    def is_email_valid(email):
        """Validate an email address."""
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    @staticmethod
    def is_url_valid(url):
        """Validate a URL."""
        url_regex = r'^(https?://)?(www\.)?([a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+)(:[0-9]{1,5})?(/.*)?$'
        return re.match(url_regex, url) is not None

    @staticmethod
    def is_password_strong(password):
        """Validate a password's strength."""
        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
        return re.match(password_regex, password) is not None

# Example usage
if __name__ == "__main__":
    validators = Validators()
    print("Email validation:", validators.is_email_valid('example@example.com'))
    print("URL validation:", validators.is_url_valid('https://example.com'))
    print("Password strength:", validators.is_password_strong('MyStrongP@ssw0rd'))
