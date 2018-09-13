import string


def clean_input(text):
    ''' this method cleans an input an ensures that a string was submitted '''
    """ ensure that it's a string"""
    text = str(text)

    """ specify the characters to remove"""

    chars = string.whitespace + string.punctuation + string.digits

    """ remove the characters and return the result"""

    return text.strip(chars)
