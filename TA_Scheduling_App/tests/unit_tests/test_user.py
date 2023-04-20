import sys
from TA_Scheduling_App.classes.user import User
import unittest

class TestSetFirstName(unittest.TestCase):
    def setUp(self):
        self.user = User(userID=1, userType='TA', firstName='Jane', lastName='Doe', email='jane.doe@example.com',
                          phoneNumber='555-123-4567', address='1234 Elm St', birthDate='1995-08-30')
    def test_setFirstName_valid(self):
        self.assertTrue(self.user.setFirstName("John"))

    def test_setFirstName_valid_with_spaces(self):
        self.assertTrue(self.user.setFirstName("John Smith"))

    def test_setFirstName_valid_with_hyphen(self):
        self.assertTrue(self.user.setFirstName("John-Smith"))

    def test_setFirstName_valid_with_apostrophe(self):
        self.assertTrue(self.user.setFirstName("John's"))

    def test_setFirstName_invalid_empty_string(self):
        self.assertFalse(self.user.setFirstName(""))

    def test_setFirstName_invalid_whitespace(self):
        self.assertFalse(self.user.setFirstName("   "))

    def test_setFirstName_invalid_special_characters(self):
        self.assertFalse(self.user.setFirstName("#$%@"))

    def test_setFirstName_invalid_numbers(self):
        self.assertFalse(self.user.setFirstName("1234"))

    def test_setFirstName_invalid_combination(self):
        self.assertFalse(self.user.setFirstName("John1234"))

    def test_setFirstName_valid_unicode(self):
        self.assertTrue(self.user.setFirstName("Élodie"))

    def test_setFirstName_valid_mixed_case(self):
        self.assertTrue(self.user.setFirstName("jOhN"))

    def test_setFirstName_valid_spaces_before_after(self):
        self.assertTrue(self.user.setFirstName("  John  "))

    def test_setFirstName_invalid_only_numbers(self):
        self.assertFalse(self.user.setFirstName("1234"))

    def test_setFirstName_invalid_long_string(self):
        self.assertFalse(self.user.setFirstName("a" * 256))

    def test_setFirstName_valid_one_letter(self):
        self.assertTrue(self.user.setFirstName("J"))

class TestSetLastName(unittest.TestCase):
    def setUp(self):
        self.user = User(userID=1, userType='TA', firstName='Jane', lastName='Doe', email='jane.doe@example.com',
                          phoneNumber='555-123-4567', address='1234 Elm St', birthDate='1995-08-30')

    def test_setLastName_valid(self):
        self.assertTrue(self.user.setLastName("Smith"))

    def test_setLastName_valid_with_spaces(self):
        self.assertTrue(self.user.setLastName("Smith Johnson"))

    def test_setLastName_valid_with_hyphen(self):
        self.assertTrue(self.user.setLastName("Smith-Johnson"))

    def test_setLastName_valid_with_apostrophe(self):
        self.assertTrue(self.user.setLastName("O'Connor"))

    def test_setLastName_invalid_empty_string(self):
        self.assertFalse(self.user.setLastName(""))

    def test_setLastName_invalid_whitespace(self):
        self.assertFalse(self.user.setLastName("   "))

    def test_setLastName_invalid_special_characters(self):
        self.assertFalse(self.user.setLastName("#$%@"))

    def test_setLastName_invalid_numbers(self):
        self.assertFalse(self.user.setLastName("1234"))

    def test_setLastName_invalid_combination(self):
        self.assertFalse(self.user.setLastName("Smith1234"))

    def test_setLastName_valid_unicode(self):
        self.assertTrue(self.user.setLastName("Åström"))

    def test_setLastName_valid_mixed_case(self):
        self.assertTrue(self.user.setLastName("sMitH"))

    def test_setLastName_valid_spaces_before_after(self):
        self.assertTrue(self.user.setLastName("  Smith  "))

    def test_setLastName_invalid_only_numbers(self):
        self.assertFalse(self.user.setLastName("1234"))

    def test_setLastName_invalid_long_string(self):
        self.assertFalse(self.user.setLastName("a" * 256))

    def test_setLastName_valid_one_letter(self):
        self.assertTrue(self.user.setLastName("S"))

class TestSetEmail(unittest.TestCase):
    def setUp(self):
        self.user1 = User(userID=1, userType='TA', firstName='Jane', lastName='Doe', email='jane.doe@example.com',
                          phoneNumber='555-123-4567', address='1234 Elm St', birthDate='1995-08-30')

        self.user2 = User(userID=2, userType='Professor', firstName='John', lastName='Smith', email='john.smith@example.com',
                          phoneNumber='555-987-6543', address='5678 Oak St', birthDate='1980-01-15')
    def test_setEmail_valid(self):
        self.assertTrue(self.user1.setEmail("john.smith@example.com"))

    def test_setEmail_invalid_empty_string(self):
        self.assertFalse(self.user1.setEmail(""))

    def test_setEmail_invalid_no_at_symbol(self):
        self.assertFalse(self.user1.setEmail("john.smithexample.com"))

    def test_setEmail_invalid_no_domain(self):
        self.assertFalse(self.user1.setEmail("john.smith@"))

    def test_setEmail_invalid_no_username(self):
        self.assertFalse(self.user1.setEmail("@example.com"))

    def test_setEmail_invalid_multiple_at_symbols(self):
        self.assertFalse(self.user1.setEmail("john@smith@example.com"))

    def test_setEmail_invalid_whitespace(self):
        self.assertFalse(self.user1.setEmail("john.smith @example.com"))

    def test_setEmail_invalid_missing_tld(self):
        self.assertFalse(self.user1.setEmail("john.smith@example"))

    def test_setEmail_invalid_domain_start_with_period(self):
        self.assertFalse(self.user1.setEmail("john.smith@.example.com"))

    def test_setEmail_invalid_domain_end_with_period(self):
        self.assertFalse(self.user1.setEmail("john.smith@example.com."))

    def test_setEmail_invalid_domain_multiple_periods(self):
        self.assertFalse(self.user1.setEmail("john.smith@example..com"))

    def test_setEmail_valid_mixed_case(self):
        self.assertTrue(self.user1.setEmail("JOHN.Smith@example.com"))

    def test_setEmail_valid_unicode(self):
        self.assertTrue(self.user1.setEmail("jane.åström@example.com"))

    def test_setEmail_valid_subdomain(self):
        self.assertTrue(self.user1.setEmail("jane.doe@subdomain.example.com"))

    def test_setEmail_invalid_long_string(self):
        self.assertFalse(self.user1.setEmail("a" * 256 + "@example.com"))

    def test_setEmail_valid_underscore(self):
        self.assertTrue(self.user1.setEmail("john_smith@example.com"))

    def test_setEmail_valid_dash(self):
        self.assertTrue(self.user1.setEmail("john-smith@example.com"))

    def test_setEmail_invalid_username_start_with_period(self):
        self.assertFalse(self.user1.setEmail(".john.smith@example.com"))

    def test_setEmail_unique_emails(self):
        self.assertTrue(self.user1.setEmail("new.email@example.com"))
        self.assertFalse(self.user2.setEmail("new.email@example.com"))

class TestSetPhoneNumber(unittest.TestCase):
    def setUp(self):
        self.user = User(userID=1, userType='TA', firstName='Jane', lastName='Doe', email='jane.doe@example.com',
                          phoneNumber='555-123-4567', address='1234 Elm St', birthDate='1995-08-30')

    def test_setPhoneNumber_valid(self):
        self.assertTrue(self.user.setPhoneNumber("555-987-6543"))

    def test_setPhoneNumber_valid_no_dash(self):
        self.assertTrue(self.user.setPhoneNumber("5559876543"))

    def test_setPhoneNumber_valid_with_spaces(self):
        self.assertTrue(self.user.setPhoneNumber("555 987 6543"))

    def test_setPhoneNumber_valid_with_parentheses(self):
        self.assertTrue(self.user.setPhoneNumber("(555) 987-6543"))

    def test_setPhoneNumber_valid_with_country_code(self):
        self.assertTrue(self.user.setPhoneNumber("+1-555-987-6543"))

    def test_setPhoneNumber_invalid_empty_string(self):
        self.assertFalse(self.user.setPhoneNumber(""))

    def test_setPhoneNumber_invalid_whitespace(self):
        self.assertFalse(self.user.setPhoneNumber("  "))

    def test_setPhoneNumber_invalid_too_long(self):
        self.assertFalse(self.user.setPhoneNumber("555-987-6543" * 5))

    def test_setPhoneNumber_invalid_special_characters(self):
        self.assertFalse(self.user.setPhoneNumber("555!987$6543"))

    def test_setPhoneNumber_invalid_letters(self):
        self.assertFalse(self.user.setPhoneNumber("555-abc-efgh"))

    def test_setPhoneNumber_invalid_combination(self):
        self.assertFalse(self.user.setPhoneNumber("555-abc-1234"))

    def test_setPhoneNumber_invalid_long_string(self):
        self.assertFalse(self.user.setPhoneNumber("1" * 21))

    def test_setPhoneNumber_valid_mixed_formats(self):
        self.assertTrue(self.user.setPhoneNumber("+1 (555) 987-6543"))

    def test_setPhoneNumber_invalid_missing_digits_1(self):
        self.assertFalse(self.user.setPhoneNumber("55-987-6543"))

    def test_setPhoneNumber_invalid_missing_digits_2(self):
        self.assertFalse(self.user.setPhoneNumber("555-98-6543"))

    def test_setPhoneNumber_invalid_missing_digits_3(self):
        self.assertFalse(self.user.setPhoneNumber("555-987-643"))

    def test_setPhoneNumber_invalid_extra_digits_1(self):
        self.assertFalse(self.user.setPhoneNumber("5555-987-6543"))

    def test_setPhoneNumber_invalid_extra_digits_2(self):
        self.assertFalse(self.user.setPhoneNumber("555-9877-6543"))

    def test_setPhoneNumber_invalid_extra_digits_3(self):
        self.assertFalse(self.user.setPhoneNumber("555-987-65433"))

    def test_setPhoneNumber_invalid_extra_digits_3(self):
        self.assertFalse(self.user.setPhoneNumber("555-987-65433"))

    def test_setPhoneNumber_valid_max_length(self):
        self.assertTrue(self.user.setPhoneNumber("+123 (456) 789-0123"))

class TestSetAddress(unittest.TestCase):
    def setUp(self):
        self.user = User(userID=1, userType='TA', firstName='Jane', lastName='Doe', email='jane.doe@example.com',
                          phoneNumber='555-123-4567', address='1234 Elm St', birthDate='1995-08-30')

    def test_setAddress_valid(self):
        self.assertTrue(self.user.setAddress("5678 Oak St"))

    def test_setAddress_valid_with_numbers(self):
        self.assertTrue(self.user.setAddress("1234 Elm St, Apt 56"))

    def test_setAddress_valid_with_commas(self):
        self.assertTrue(self.user.setAddress("1234 Elm St, Suite 100"))

    def test_setAddress_valid_with_special_characters(self):
        self.assertTrue(self.user.setAddress("1234 Elm St, #2B"))

    def test_setAddress_valid_with_long_street_name(self):
        self.assertTrue(self.user.setAddress("1234 This Is A Very Long Street Name St"))

    def test_setAddress_invalid_empty_string(self):
        self.assertFalse(self.user.setAddress(""))

    def test_setAddress_invalid_whitespace(self):
        self.assertFalse(self.user.setAddress("    "))

    def test_setAddress_invalid_only_special_characters(self):
        self.assertFalse(self.user.setAddress("@#$%^&*"))

    def test_setAddress_invalid_long_string(self):
        self.assertFalse(self.user.setAddress("a" * 256))

    def test_setAddress_valid_mixed_case(self):
        self.assertTrue(self.user.setAddress("1234 eLM St"))

    def test_setAddress_valid_spaces_before_after(self):
        self.assertTrue(self.user.setAddress("  1234 Elm St  "))

    def test_setAddress_valid_unicode(self):
        self.assertTrue(self.user.setAddress("1234 Åvägen"))

    def test_setAddress_valid_with_dash(self):
        self.assertTrue(self.user.setAddress("1234-1236 Elm St"))

    def test_setAddress_valid_with_multiple_lines(self):
        self.assertTrue(self.user.setAddress("1234 Elm St\nApt 9"))

    def test_setAddress_valid_with_po_box(self):
        self.assertTrue(self.user.setAddress("PO Box 123"))
