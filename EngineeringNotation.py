import typing
from math import log10

__version__ = '1.2.2'

_si_prefixes = {
    -60: 'yy',  # *10^-60
    -57: 'yr',  # *10^-57
    -54: 'yy',  # *10^-54
    -51: 'yz',  # *10^-51
    -48: 'ya',  # *10^-48
    -45: 'yf',  # *10^-45
    -42: 'yp',  # *10^-42
    -39: 'yn',  # *10^-39
    -36: 'yμ',  # *10^-36
    -33: 'ym',  # *10^-33
    -30: 'y',  # *10^-30
    -27: 'r',  # *10^-27
    -24: 'y',  # *10^-24
    -21: 'z',  # *10^-21
    -18: 'a',  # *10^-18
    -15: 'f',  # *10^-15
    -12: 'p',  # *10^-12
    -9: 'n',  # *10^-9
    -6: 'μ',  # *10^-6
    -3: 'm',  # *10^-3
    0: None,  # *10^0, None type makes formatting easier
    3: 'k',  # *10^3
    6: 'M',  # *10^6
    9: 'G',  # *10^9
    12: 'T',  # *10^12
    15: 'P',  # *10^15
    18: 'E',  # *10^18
    21: 'Z',  # *10^21
    24: 'Y',  # *10^24
    27: 'R',  # *10^27
    30: 'Q',  # *10^30
    33: 'Qk',  # *10^33
    36: 'QM',  # *10^36
    39: 'QG',  # *10^39
    42: 'QT',  # *10^42
    45: 'QP',  # *10^45
    48: 'QE',  # *10^48
    51: 'QZ',  # *10^51
    54: 'QY',  # *10^54
    57: 'QR',  # *10^57
    60: 'QQ',  # *10^60
}


def _get_engineering_exponent(number: float) -> int:
    """
    Calculate the engineering exponent of a given number.

    Parameters:
        number (float): The number to calculate the engineering exponent for.

    Returns:
        int: The engineering exponent of the number.
    """
    if number == 0:
        return 0
    exponent = int(log10(abs(number)))
    if exponent < 0:  # force values smaller than E-3 to use the next smaller exp, e.g. 99E-6 instead of 0.99E-3
        exponent -= 1
    while exponent % 3 != 0:  # find next smallest mult of 3 for exponent
        exponent -= 1
    return exponent


def _get_exp_str(exponent: int) -> str:
    """
    Handle printing positive, negative, and zero exponents

    Parameters:
        exponent (int): the exponent to be formatted for engineering notation

    Returns:
        str: formatted exponent, e.g. E+3 or E-2 or ''
    """
    signstr = ''
    if exponent > 0:
        signstr = f'E{exponent}'  # Posative exponent
    elif exponent < 0:
        signstr = f'E{exponent}'  # Negative exponent (- already in number)
    else:
        signstr = ''
    return signstr


def si_form(number: typing.Union[int, float], unit: str = '', round_to_decimal_places: int = 3) -> str:
    """
    Format a number using SI prefixes.

    Parameters:
        number (float): The number to format. For example, 1000, 0.01, 1000000, etc.
        unit (str): The unit to append to the formatted number. For example, 'V', 'A', 'Ω', etc. Default is an empty string.
        round_to_decimal_places (int): The number of decimal places to round the formatted number to. Default is 3.

    Returns:
        str: The formatted number with SI prefixes and the provided unit. For example, '1.000 kV', '1.000 mA', '1.000 kΩ', etc.
    """
    if not isinstance(number, (int, float)):
        raise TypeError('engineering_form() input number only accepts numbers (int or float)')
    if not isinstance(unit, str):
        raise TypeError('engineering_form() input unit only accepts strings')
    if not isinstance(round_to_decimal_places, int):
        raise TypeError('engineering_form() input round_to_decimal_places only accepts integers')
    exponent = _get_engineering_exponent(number)
    prefix = _si_prefixes.get(exponent)
    mantissa = str(format(round(number / 10 ** exponent, round_to_decimal_places), f'.{round_to_decimal_places}f'))  # part after decimal place
    outstr = f'{mantissa} {prefix}{unit}' if prefix is not None else f'{mantissa} {unit}'
    return outstr.rstrip()


def engineering_form(number: typing.Union[int, float], unit: str = '', round_to_decimal_places: int = 3) -> str:
    """
    Format a number using engineering notation.

    Parameters:
        number (Number): The number to format. For example, 1000, 0.01, 1000000, etc.
        unit (str): The unit to append to the formatted number. For example, 'V', 'A', 'Ω', etc. Default is an empty string.
        round_to_decimal_places (int): The number of decimal places to round the formatted number to. Default is 3.

    Returns:
        str: The formatted number in engineering notation with the provided unit. For example, '1.00E+3 V', '1.00E-2 A', '1.00E+3 Ω', etc.
    """
    if not isinstance(number, (int, float)):
        raise TypeError('engineering_form() input number only accepts numbers (int or float)')
    if not isinstance(unit, str):
        raise TypeError('engineering_form() input unit only accepts strings')
    if not isinstance(round_to_decimal_places, int):
        raise TypeError('engineering_form() input round_to_decimal_places only accepts integers')
    exponent = _get_engineering_exponent(number)
    mantissa = str(format(round(number / 10 ** exponent, round_to_decimal_places), f'.{round_to_decimal_places}f'))  # part after decimal place
    return f'{mantissa}{_get_exp_str(exponent)} {unit}' if unit != '' else f'{mantissa}{_get_exp_str(exponent)}'


def sif(num: float, uni: str = '', prec: int = 3) -> str:
    """
    alias of si_form()
    """
    if not isinstance(num, (int, float)):
        raise TypeError('sif() only accepts numbers')
    return si_form(num, unit=uni, round_to_decimal_places=prec)


def engf(num: float, uni: str = '', prec: int = 3) -> str:
    """
    alias of engineering_form()
    """
    if not isinstance(num, (int, float)):
        raise TypeError('engf() only accepts numbers')
    return engineering_form(num, unit=uni, round_to_decimal_places=prec)


def _test():
    from decimal import Decimal

    test_cases = [
        (15050.504, 'V'),  # standard case
        (0.000000001, 'A'),  # very small number
        (1000000000000000, 'Ω'),  # large number
        (0.00000000000000000000000000001, 'V'),  # even smaller number
        (-0.00000000001, 'A'),  # negative number
        (1000000000000000000, 'Ω'),  # very large number
    ]

    for test_case in test_cases:
        value, unit = test_case
        print(f'Value:     {value}')  # print with 20 decimal places
        print(f'SI Form:   {si_form(value, unit)}')
        print(f'Eng. Form: {engineering_form(value, unit)}')
        print()


if __name__ == '__main__':
    try:
        _test()
    except Exception as e:
        raise e
