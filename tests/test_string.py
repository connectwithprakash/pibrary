from pibrary.string import String


class TestString:
    """
    A test class for the CustomString class.
    """

    def test_remove_punctuation_except_period(self):
        """
        Tests the remove_punctuation_except_period method of the CustomString class.
        """
        text = String("Hello, world! This is a test.")
        assert text.remove_punctuation_except_period().str == "Hello world This is a test."

    def test_remove_punctuation(self):
        """
        Tests the remove_punctuation method of the CustomString class.
        """
        text = String("Hello, world! This is a test.")
        assert text.remove_punctuation().str == "Hello world This is a test"

    def test_remove_digits(self):
        """
        Tests the remove_digits method of the CustomString class.
        """
        text = String("The price is $9.99")
        assert text.remove_digits().str == "The price is $."

    def test_remove_duplicate_spaces(self):
        """
        Tests the remove_duplicate_spaces method of the CustomString class.
        """
        text = String("   Hello   world!   ")
        assert text.remove_duplicate_spaces().str == "Hello world!"
