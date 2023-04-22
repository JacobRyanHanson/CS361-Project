import sys
import os
import django
import unittest
import datetime

# Set up the Django settings module for testing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TA_Scheduling_Project.settings')
django.setup()

from TA_Scheduling_App.models.User import User

class TestSetRoll(unittest.TestCase):
    def setUp(self):
        self.user = User(ROLL='TA', FIRST_NAME='Jane', LAST_NAME='Doe', EMAIL='jane.doe@example.com',
                         PHONE_NUMBER='555-123-4567', ADDRESS='1234 Elm St', BIRTH_DATE='1995-08-30')

    def test_setRoll_valid_admin(self):
        self.assertTrue(self.user.setRoll("ADMIN"), "Valid roll 'ADMIN' failed to be set.")

    def test_setRoll_valid_instructor(self):
        self.assertTrue(self.user.setRoll("INSTRUCTOR"), "Valid roll 'INSTRUCTOR' failed to be set.")

    def test_setRoll_valid_ta(self):
        self.assertTrue(self.user.setRoll("TA"), "Valid roll 'TA' failed to be set.")

    def test_setRoll_invalid_empty_string(self):
        self.assertFalse(self.user.setRoll(""), "Empty roll string was incorrectly set.")

    def test_setRoll_invalid_whitespace(self):
        self.assertFalse(self.user.setRoll("   "), "Roll with only whitespace was incorrectly set.")

    def test_setRoll_invalid_lowercase(self):
        self.assertFalse(self.user.setRoll("admin"), "Lowercase roll string was incorrectly set.")

    def test_setRoll_invalid_mixed_case(self):
        self.assertFalse(self.user.setRoll("AdMiN"), "Mixed case roll string was incorrectly set.")

    def test_setRoll_invalid_numbers(self):
        self.assertFalse(self.user.setRoll("1234"), "Roll with numbers was incorrectly set.")

    def test_setRoll_invalid_special_characters(self):
        self.assertFalse(self.user.setRoll("#$%@"), "Roll with special characters was incorrectly set.")

    def test_setRoll_invalid_other_string(self):
        self.assertFalse(self.user.setRoll("STUDENT"), "Invalid roll string was incorrectly set.")

    def test_setRoll_invalid_spaces_before_after(self):
        self.assertFalse(self.user.setRoll("  ADMIN  "), "Roll with spaces before and after was incorrectly set.")

    def test_setRoll_invalid_combination(self):
        self.assertFalse(self.user.setRoll("ADMIN123"), "Roll with letters and numbers was incorrectly set.")

    def test_setRoll_invalid_unicode(self):
        self.assertFalse(self.user.setRoll("ÄDMIN"), "Roll with unicode characters was incorrectly set.")

    def test_setRoll_invalid_long_string(self):
        self.assertFalse(self.user.setRoll("A" * 256), "Roll with too long string was incorrectly set.")

    def test_setRoll_invalid_one_letter(self):
        self.assertFalse(self.user.setRoll("A"), "Roll with only one letter was incorrectly set.")

    def test_setRoll_invalid_null(self):
        self.assertFalse(self.user.setRoll(None), "Null roll was incorrectly set.")
        

class TestSetFirstName(unittest.TestCase):
    def setUp(self):
        self.user = User(ROLL='TA', FIRST_NAME='Jane', LAST_NAME='Doe', EMAIL='jane.doe@example.com',
                         PHONE_NUMBER='555-123-4567', ADDRESS='1234 Elm St', BIRTH_DATE='1995-08-30')

    def test_setFirstName_valid(self):
        self.assertTrue(self.user.setFirstName("John"), "Valid first name failed to be set.")

    def test_setFirstName_valid_with_spaces(self):
        self.assertTrue(self.user.setFirstName("John Smith"), "Valid first name with spaces failed to be set.")

    def test_setFirstName_valid_with_hyphen(self):
        self.assertTrue(self.user.setFirstName("John-Smith"), "Valid first name with hyphen failed to be set.")

    def test_setFirstName_valid_with_apostrophe(self):
        self.assertTrue(self.user.setFirstName("John's"), "Valid first name with apostrophe failed to be set.")

    def test_setFirstName_invalid_empty_string(self):
        self.assertFalse(self.user.setFirstName(""), "Empty first name was incorrectly set.")

    def test_setFirstName_invalid_whitespace(self):
        self.assertFalse(self.user.setFirstName("   "), "First name with only whitespace was incorrectly set.")

    def test_setFirstName_invalid_special_characters(self):
        self.assertFalse(self.user.setFirstName("#$%@"), "First name with special characters was incorrectly set.")

    def test_setFirstName_invalid_numbers(self):
        self.assertFalse(self.user.setFirstName("1234"), "First name with numbers was incorrectly set.")

    def test_setFirstName_invalid_combination(self):
        self.assertFalse(self.user.setFirstName("John1234"), "First name with numbers and letters was incorrectly set.")

    def test_setFirstName_valid_unicode(self):
        self.assertTrue(self.user.setFirstName("Élodie"), "Valid first name with unicode characters failed to be set.")

    def test_setFirstName_valid_mixed_case(self):
        self.assertTrue(self.user.setFirstName("jOhN"), "Valid first name with mixed case failed to be set.")

    def test_setFirstName_valid_spaces_before_after(self):
        self.assertTrue(self.user.setFirstName("  John  "),
                        "Valid first name with spaces before and after failed to be set.")

    def test_setFirstName_invalid_only_numbers(self):
        self.assertFalse(self.user.setFirstName("1234"), "First name with only numbers was incorrectly set.")

    def test_setFirstName_invalid_long_string(self):
        self.assertFalse(self.user.setFirstName("a" * 256), "First name that is too long was incorrectly set.")

    def test_setFirstName_valid_one_letter(self):
        self.assertTrue(self.user.setFirstName("J"), "Valid first name with only one letter failed to be set.")

    def test_setFirstName_invalid_null(self):
        self.assertFalse(self.user.setFirstName(None), "Null first name was incorrectly set.")


class TestSetLastName(unittest.TestCase):
    def setUp(self):
        self.user = User(ROLL='TA', FIRST_NAME='Jane', LAST_NAME='Doe', EMAIL='jane.doe@example.com',
                         PHONE_NUMBER='555-123-4567', ADDRESS='1234 Elm St', BIRTH_DATE='1995-08-30')

    def test_setLastName_valid(self):
        self.assertTrue(self.user.setLastName("Smith"), "Valid last name failed to be set.")

    def test_setLastName_valid_with_spaces(self):
        self.assertTrue(self.user.setLastName("Smith Johnson"), "Valid last name with spaces failed to be set.")

    def test_setLastName_valid_with_hyphen(self):
        self.assertTrue(self.user.setLastName("Smith-Johnson"), "Valid last name with hyphen failed to be set.")

    def test_setLastName_valid_with_apostrophe(self):
        self.assertTrue(self.user.setLastName("O'Connor"), "Valid last name with apostrophe failed to be set.")

    def test_setLastName_invalid_empty_string(self):
        self.assertFalse(self.user.setLastName(""), "Empty last name was incorrectly set.")

    def test_setLastName_invalid_whitespace(self):
        self.assertFalse(self.user.setLastName("   "), "Last name with only whitespace was incorrectly set.")

    def test_setLastName_invalid_special_characters(self):
        self.assertFalse(self.user.setLastName("#$%@"), "Last name with special characters was incorrectly set.")

    def test_setLastName_invalid_numbers(self):
        self.assertFalse(self.user.setLastName("1234"), "Last name with numbers was incorrectly set.")

    def test_setLastName_invalid_combination(self):
        self.assertFalse(self.user.setLastName("Smith1234"), "Last name with numbers and letters was incorrectly set.")

    def test_setLastName_valid_unicode(self):
        self.assertTrue(self.user.setLastName("Åström"), "Valid last name with unicode characters failed to be set.")

    def test_setLastName_valid_mixed_case(self):
        self.assertTrue(self.user.setLastName("sMitH"), "Valid last name with mixed case failed to be set.")

    def test_setLastName_valid_spaces_before_after(self):
        self.assertTrue(self.user.setLastName("  Smith  "),
                        "Valid last name with spaces before and after failed to be set.")

    def test_setLastName_invalid_only_numbers(self):
        self.assertFalse(self.user.setLastName("1234"), "Last name with only numbers was incorrectly set.")

    def test_setLastName_invalid_long_string(self):
        self.assertFalse(self.user.setLastName("a" * 256), "Last name that is too long was incorrectly set.")

    def test_setLastName_valid_one_letter(self):
        self.assertTrue(self.user.setLastName("S"), "Valid last name with only one letter failed to be set.")

    def test_setLastName_invalid_null(self):
        self.assertFalse(self.user.setLastName(None), "Null last name was incorrectly set.")


class TestSetEmail(unittest.TestCase):
    def setUp(self):
        self.user1 = User(ROLL='TA', FIRST_NAME='Jane', LAST_NAME='Doe', EMAIL='jane.doe@example.com',
                         PHONE_NUMBER='555-123-4567', ADDRESS='1234 Elm St', BIRTH_DATE='1995-08-30')

        self.user2 = User(ROLL='Professor', FIRST_NAME='John', LAST_NAME='Smith', EMAIL='john.smith@example.com',
                          PHONE_NUMBER='555-987-6543', ADDRESS='5678 Oak St', BIRTH_DATE='1980-01-15')

    def test_setEmail_valid(self):
        self.assertTrue(self.user1.setEmail("john.smith@example.com"), "Valid email failed to be set.")

    def test_setEmail_invalid_empty_string(self):
        self.assertFalse(self.user1.setEmail(""), "Empty email was incorrectly set.")

    def test_setEmail_invalid_no_at_symbol(self):
        self.assertFalse(self.user1.setEmail("john.smithexample.com"), "Email without @ symbol was incorrectly set.")

    def test_setEmail_invalid_no_domain(self):
        self.assertFalse(self.user1.setEmail("john.smith@"), "Email without domain was incorrectly set.")

    def test_setEmail_invalid_no_username(self):
        self.assertFalse(self.user1.setEmail("@example.com"), "Email without username was incorrectly set.")

    def test_setEmail_invalid_multiple_at_symbols(self):
        self.assertFalse(self.user1.setEmail("john@smith@example.com"),
                         "Email with multiple @ symbols was incorrectly set.")

    def test_setEmail_invalid_whitespace(self):
        self.assertFalse(self.user1.setEmail("john.smith @example.com"), "Email with whitespace was incorrectly set.")

    def test_setEmail_invalid_missing_tld(self):
        self.assertFalse(self.user1.setEmail("john.smith@example"),
                         "Email with missing top-level domain was incorrectly set.")

    def test_setEmail_invalid_domain_start_with_period(self):
        self.assertFalse(self.user1.setEmail("john.smith@.example.com"),
                         "Email with domain starting with a period was incorrectly set.")

    def test_setEmail_invalid_domain_end_with_period(self):
        self.assertFalse(self.user1.setEmail("john.smith@example.com."),
                         "Email with domain ending with a period was incorrectly set.")

    def test_setEmail_invalid_domain_multiple_periods(self):
        self.assertFalse(self.user1.setEmail("john.smith@example..com"),
                         "Email with domain containing multiple periods was incorrectly set.")

    def test_setEmail_valid_mixed_case(self):
        self.assertTrue(self.user1.setEmail("JOHN.Smith@example.com"), "Valid email with mixed case failed to be set.")

    def test_setEmail_valid_unicode(self):
        self.assertTrue(self.user1.setEmail("jane.åström@example.com"),
                        "Valid email with unicode characters failed to be set.")

    def test_setEmail_valid_subdomain(self):
        self.assertTrue(self.user1.setEmail("jane.doe@subdomain.example.com"),
                        "Valid email with subdomain failed to be set.")

    def test_setEmail_invalid_long_string(self):
        self.assertFalse(self.user1.setEmail("a" * 256 + "@example.com"), "Email that is too long was incorrectly set.")

    def test_setEmail_valid_underscore(self):
        self.assertTrue(self.user1.setEmail("john_smith@example.com"), "Valid email with underscore failed to be set.")

    def test_setEmail_valid_dash(self):
        self.assertTrue(self.user1.setEmail("john-smith@example.com"), "Valid email with dash failed to be set.")

    def test_setEmail_invalid_username_start_with_period(self):
        self.assertFalse(self.user1.setEmail(".john.smith@example.com"),
                         "Email with username starting with a period was incorrectly set.")

    def test_setEmail_unique_emails(self):
        self.assertTrue(self.user1.setEmail("new.email@example.com"), "Valid new email failed to be set.")
        self.assertFalse(self.user2.setEmail("new.email@example.com"), "Duplicate email was incorrectly set for a different user.")

    def test_setEmail_invalid_null(self):
        self.assertFalse(self.user1.setEmail(None), "Null email was incorrectly set.")


class TestSetPhoneNumber(unittest.TestCase):
    def setUp(self):
        self.user = User(ROLL='TA', FIRST_NAME='Jane', LAST_NAME='Doe', EMAIL='jane.doe@example.com',
                         PHONE_NUMBER='555-123-4567', ADDRESS='1234 Elm St', BIRTH_DATE='1995-08-30')

    def test_setPhoneNumber_valid(self):
        self.assertTrue(self.user.setPhoneNumber("555-987-6543"), "Valid phone number failed to be set.")

    def test_setPhoneNumber_valid_no_dash(self):
        self.assertTrue(self.user.setPhoneNumber("5559876543"), "Valid phone number without dashes failed to be set.")

    def test_setPhoneNumber_valid_with_spaces(self):
        self.assertTrue(self.user.setPhoneNumber("555 987 6543"), "Valid phone number with spaces failed to be set.")

    def test_setPhoneNumber_valid_with_parentheses(self):
        self.assertTrue(self.user.setPhoneNumber("(555) 987-6543"),
                        "Valid phone number with parentheses failed to be set.")

    def test_setPhoneNumber_valid_with_country_code(self):
        self.assertTrue(self.user.setPhoneNumber("+1-555-987-6543"),
                        "Valid phone number with country code failed to be set.")

    def test_setPhoneNumber_invalid_empty_string(self):
        self.assertFalse(self.user.setPhoneNumber(""), "Empty phone number was incorrectly set.")

    def test_setPhoneNumber_invalid_whitespace(self):
        self.assertFalse(self.user.setPhoneNumber("  "), "Phone number with only whitespace was incorrectly set.")

    def test_setPhoneNumber_invalid_too_long(self):
        self.assertFalse(self.user.setPhoneNumber("555-987-6543" * 5),
                         "Phone number that is too long was incorrectly set.")

    def test_setPhoneNumber_invalid_special_characters(self):
        self.assertFalse(self.user.setPhoneNumber("555!987$6543"),
                         "Phone number with special characters was incorrectly set.")

    def test_setPhoneNumber_invalid_letters(self):
        self.assertFalse(self.user.setPhoneNumber("555-abc-efgh"), "Phone number with letters was incorrectly set.")

    def test_setPhoneNumber_invalid_combination(self):
        self.assertFalse(self.user.setPhoneNumber("555-abc-1234"),
                         "Phone number with invalid combination was incorrectly set.")

    def test_setPhoneNumber_invalid_long_string(self):
        self.assertFalse(self.user.setPhoneNumber("1" * 21), "Phone number that is too long was incorrectly set.")

    def test_setPhoneNumber_valid_mixed_formats(self):
        self.assertTrue(self.user.setPhoneNumber("+1 (555) 987-6543"),
                        "Valid phone number with mixed formats failed to be set.")

    def test_setPhoneNumber_invalid_missing_digits_1(self):
        self.assertFalse(self.user.setPhoneNumber("55-987-6543"),
                         "Phone number with missing digits was incorrectly set.")

    def test_setPhoneNumber_invalid_missing_digits_2(self):
        self.assertFalse(self.user.setPhoneNumber("555-98-6543"),
                         "Phone number with missing digits was incorrectly set.")

    def test_setPhoneNumber_invalid_missing_digits_3(self):
        self.assertFalse(self.user.setPhoneNumber("555-987-643"),
                         "Phone number with missing digits was incorrectly set.")

    def test_setPhoneNumber_invalid_extra_digits_1(self):
        self.assertFalse(self.user.setPhoneNumber("5555-987-6543"),
                         "Phone number with extra digits was incorrectly set.")

    def test_setPhoneNumber_invalid_extra_digits_2(self):
        self.assertFalse(self.user.setPhoneNumber("555-9877-6543"),
                         "Phone number with extra digits was incorrectly set.")

    def test_setPhoneNumber_invalid_extra_digits_3(self):
        self.assertFalse(self.user.setPhoneNumber("555-987-65433"),
                         "Phone number with extra digits was incorrectly set.")

    def test_setPhoneNumber_valid_max_length(self):
        self.assertTrue(self.user.setPhoneNumber("+123 (456) 789-0123"), "Phone number with max length failed to be set.")

    def test_setPhoneNumber_invalid_null(self):
        self.assertFalse(self.user.setPhoneNumber(None), "Null phone number was incorrectly set.")


class TestSetAddress(unittest.TestCase):
    def setUp(self):
        self.user = User(ROLL='TA', FIRST_NAME='Jane', LAST_NAME='Doe', EMAIL='jane.doe@example.com',
                          PHONE_NUMBER='555-123-4567', ADDRESS='1234 Elm St', BIRTH_DATE='1995-08-30')

    def test_setAddress_valid(self):
        self.assertTrue(self.user.setAddress("5678 Oak St"), "Valid address failed to be set.")

    def test_setAddress_valid_with_numbers(self):
        self.assertTrue(self.user.setAddress("1234 Elm St, Apt 56"), "Valid address with numbers failed to be set.")

    def test_setAddress_valid_with_commas(self):
        self.assertTrue(self.user.setAddress("1234 Elm St, Suite 100"), "Valid address with commas failed to be set.")

    def test_setAddress_valid_with_special_characters(self):
        self.assertTrue(self.user.setAddress("1234 Elm St, #2B"),
                        "Valid address with special characters failed to be set.")

    def test_setAddress_valid_with_long_street_name(self):
        self.assertTrue(self.user.setAddress("1234 This Is A Very Long Street Name St"),
                        "Valid address with long street name failed to be set.")

    def test_setAddress_invalid_empty_string(self):
        self.assertFalse(self.user.setAddress(""), "Empty address was incorrectly set.")

    def test_setAddress_invalid_whitespace(self):
        self.assertFalse(self.user.setAddress("    "), "Address with only whitespace was incorrectly set.")

    def test_setAddress_invalid_only_special_characters(self):
        self.assertFalse(self.user.setAddress("@#$%^&*"), "Address with only special characters was incorrectly set.")

    def test_setAddress_invalid_long_string(self):
        self.assertFalse(self.user.setAddress("a" * 256), "Address that is too long was incorrectly set.")

    def test_setAddress_valid_mixed_case(self):
        self.assertTrue(self.user.setAddress("1234 eLM St"), "Valid address with mixed case failed to be set.")

    def test_setAddress_valid_spaces_before_after(self):
        self.assertTrue(self.user.setAddress("  1234 Elm St  "),
                        "Valid address with spaces before and after failed to be set.")

    def test_setAddress_valid_unicode(self):
        self.assertTrue(self.user.setAddress("1234 Åvägen"), "Valid address with unicode characters failed to be set.")

    def test_setAddress_valid_with_dash(self):
        self.assertTrue(self.user.setAddress("1234-1236 Elm St"), "Valid address with dash failed to be set.")

    def test_setAddress_valid_with_multiple_lines(self):
        self.assertTrue(self.user.setAddress("1234 Elm St\nApt 9"),
                        "Valid address with multiple lines failed to be set.")

    def test_setAddress_valid_with_po_box(self):
        self.assertTrue(self.user.setAddress("PO Box 123"), "Valid address with PO box failed to be set.")

    def test_setAddress_invalid_null(self):
        self.assertFalse(self.user.setAddress(None), "Null address was incorrectly set.")


class TestSetBirthDate(unittest.TestCase):
    def setUp(self):
        self.user = User(ROLL='TA', FIRST_NAME='Jane', LAST_NAME='Doe', EMAIL='jane.doe@example.com',
                          PHONE_NUMBER='555-123-4567', ADDRESS='1234 Elm St', BIRTH_DATE='1995-08-30')

    def test_setBirthDate_valid(self):
        self.assertTrue(self.user.setBirthDate(datetime.date(2000, 1, 1)), "Failed to set valid birth date")

    def test_setBirthDate_valid_leap_year(self):
        self.assertTrue(self.user.setBirthDate(datetime.date(2000, 2, 29)),
                        "Failed to set valid birth date on leap year")

    def test_setBirthDate_invalid_leap_year(self):
        self.assertFalse(self.user.setBirthDate(datetime.date(1900, 2, 29)), "Set birth date on an invalid leap year")

    def test_setBirthDate_valid_first_day_of_year(self):
        self.assertTrue(self.user.setBirthDate(datetime.date(2000, 1, 1)),
                        "Failed to set valid birth date on the first day of year")

    def test_setBirthDate_valid_last_day_of_year(self):
        self.assertTrue(self.user.setBirthDate(datetime.date(2000, 12, 31)),
                        "Failed to set valid birth date on the last day of year")

    def test_setBirthDate_valid_min_date(self):
        self.assertTrue(self.user.setBirthDate(datetime.date(1, 1, 1)),
                        "Failed to set valid birth date on the minimum date value")

    def test_setBirthDate_valid_max_date(self):
        self.assertTrue(self.user.setBirthDate(datetime.date(9999, 12, 31)),
                        "Failed to set valid birth date on the maximum date value")

    def test_setBirthDate_invalid_future_date(self):
        future_date = datetime.date.today() + datetime.timedelta(days=1)
        self.assertFalse(self.user.setBirthDate(future_date), "Set birth date on future date")

    def test_setBirthDate_invalid_null_date(self):
        self.assertFalse(self.user.setBirthDate(None), "Set birth date to null value")

    def test_setBirthDate_invalid_negative_year(self):
        with self.assertRaises(ValueError):
            self.user.setBirthDate(datetime.date(-1, 1, 1))
            self.fail("Allowed setting birth date with negative year")

    def test_setBirthDate_invalid_month_out_of_range(self):
        with self.assertRaises(ValueError):
            self.user.setBirthDate(datetime.date(2000, 13, 1))
            self.fail("Allowed setting birth date with month out of range")

    def test_setBirthDate_invalid_day_out_of_range(self):
        with self.assertRaises(ValueError):
            self.user.setBirthDate(datetime.date(2000, 1, 32))
            self.fail("Allowed setting birth date with day out of range")

    def test_setBirthDate_invalid_date_string(self):
        self.assertFalse(self.user.setBirthDate("1995-08-30"), "Set birth date with invalid string format")

    def test_setBirthDate_valid_datetime_object(self):
        self.assertTrue(self.user.setBirthDate(datetime.datetime(2000, 1, 1)),
                        "Failed to set valid birth date with datetime object")

    def test_setBirthDate_invalid_null(self):
        self.assertFalse(self.user.setBirthDate(None), "Set birth date to null value")

