class DataValidator:
    def validate_name(self, name: str) -> bool:
        """
        This method validates a name.
        """
        if "," in name or ":" in name:
            return False
        return True
    
    def validate_email(self, email: str) -> bool:
        """
        This method validates an email address.
        """
        if '@' not in email or '.' not in email or email.count('@') > 1 or email.split('@')[0] == '' or email.split('@')[1] == '' or email.split('@')[1].split('.')[0] == '' or email.split('@')[1].split('.')[1] == '' or "," in email or ":" in email:
            return False
        return True
    
    def validate_age(self, age: int) -> bool:
        """
        This method validates an age.
        """
        return age > 0 and age < 150
