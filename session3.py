from helpers import has_unique_characters
from fractions import Fraction
class BaseEncoder(object):

    def __init__(self, source_base = 10, to_base = 16, digit_map = '0123456789ABCDEF', source_digit_map = None):
        self.source_base = source_base
        self.to_base = to_base
        self.digit_map = digit_map
        self.source_digit_map = source_digit_map
    @property
    def source_base(self):
        return self._source_base

    @source_base.setter
    def source_base(self, source_base):
        if source_base < 2 or source_base > 36:
            raise ValueError("Invalid source base. Must lie between 2 and 36")
        else:
            self._source_base = source_base

    @property
    def to_base(self):
        return self._to_base

    @to_base.setter
    def to_base(self, to_base):
        if to_base < 2 or to_base > 36:
            raise ValueError("Invalid base to convert to. Must lie between 2 and 36")
        else:
            self._to_base = to_base

    @ property
    def digit_map(self):
        return self._digit_map

    @digit_map.setter
    def digit_map(self, digit_map):
        if len(digit_map) != self.to_base:
            raise ValueError("digit_map is of invalid length. Expected {0} but got {1}".format(self.to_base, len(digit_map)))
        elif not has_unique_characters(digit_map):
            raise ValueError("The digit map has repeating characters. please input unique characters in digit map".format(self.to_base, len(digit_map)))
        else:
            self._digit_map = digit_map

    @ property
    def source_digit_map(self):
        return self._source_digit_map

    @source_digit_map.setter
    def source_digit_map(self, source_digit_map):
        if not source_digit_map:
            self._source_digit_map = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:self.source_base]
        else:
            self._source_digit_map = source_digit_map

    def __repr__(self):
        return 'Base Encoder from base {0} to base {1}. Digits of the new base is : {2}'.format(self.source_base, self.to_base, self.digit_map)

    def decode_to_decimal(self, number):
        decimal_number = 0
        for digit in number:
            decimal_number = decimal_number*self.source_base + self.source_digit_map.index(digit)
        return decimal_number

    def encode(self, number):
        if self.source_base != 10:
            number = self.decode_to_decimal(number)
        output = []
        is_negative = number < 0
        number = abs(number)
        while number > 0:
            output.insert(0, self.digit_map[number%self.to_base])
            number = number//self.to_base

        encoded_number = ''.join(output)
        if is_negative:
            encoded_number = '-' + encoded_number
        return encoded_number

def encoded_from_base10(number, base, digit_map):
    '''
    This function returns a string encoding in the "base" for the the "number" using the "digit_map"
    Conditions that this function must satisfy:
    - 2 <= base <= 36 else raise ValueError
    - invalid base ValueError must have relevant information
    - digit_map must have sufficient length to represent the base
    - must return proper encoding for all base ranges between 2 to 36 (including)
    - must return proper encoding for all negative "numbers" (hint: this is equal to encoding for +ve number, but with - sign added)
    - the digit_map must not have any repeated character, else ValueError
    - the repeating character ValueError message must be relevant
    - you cannot use any in-built functions in the MATH module

    '''

    decimal_to_base_encoder = BaseEncoder(10, base, digit_map)

    return decimal_to_base_encoder.encode(number)


def float_equality_testing(a, b):
    '''
        This function emulates the ISCLOSE method from the MATH module, but you can't use this function
        We are going to assume:
        - rel_tol = 1e-12
        - abs_tol = 1e-05
    '''

    rel_tol = 1e-12
    abs_tol = 1e-05

    tol = max(rel_tol * max(abs(a), abs(b)), abs_tol)

    return abs(a - b) < tol


def manual_truncation_function(f_num):
    '''
    This function emulates python's MATH.TRUNC method. It ignores everything after the decimal point. 
    It must check whether f_num is of correct type before proceed. You can use inbuilt constructors like int, float, etc
    '''
    if not (isinstance(f_num, float) or isinstance(f_num, int)):
        raise ValueError("Invalid type. Must be float or int")

    is_negative = 1 if f_num < 0 else 0
    f_num = abs(f_num)
    truncated = 0
    while f_num > 1:
        truncated += 1
        f_num -=1
    return (-1)**is_negative*truncated

def manual_rounding_function(f_num):
    '''
    This function emulates python's inbuild ROUND function. You are not allowed to use ROUND function, but
    expected to write your one manually.
    '''
    if not (isinstance(f_num, float) or isinstance(f_num, int)):
        raise ValueError("Invalid type. Must be float or int")

    rounded = Fraction('%0.0f' % f_num).numerator
    return rounded

def rounding_away_from_zero(f_num):
    '''
    This function implements rounding away from zero as covered in the class
    Desperately need to use INT constructor? Well you can't. 
    Hint: use FRACTIONS and extract numerator. 
    '''
    if not (isinstance(f_num, float) or isinstance(f_num, int)):
        raise ValueError("Invalid type. Must be float or int")

    is_negative = 1 if f_num < 0 else 0
    rounded_away_from_zero = (-1)**is_negative * Fraction(manual_truncation_function(abs(f_num) + 0.5)).numerator
    return rounded_away_from_zero