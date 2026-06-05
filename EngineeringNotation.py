import typing
import math

__version__ = '1.2.3'

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
    """Calculate the engineering exponent of a given number.

    Parameters:
        number (float): The number to calculate the engineering exponent for.

    Returns:
        int: The engineering exponent of the number.
    """
    if number == 0:
        return 0
    return int(math.floor(math.log10(abs(number)) / 3) * 3)


def _get_exp_str(exponent: int) -> str:
    """
    Handle printing positive, negative, and zero exponents.
    """
    if exponent > 0:
        return f"E+{exponent}"
    if exponent < 0:
        return f"E{exponent}"
    return ""


def si_form(
    number: typing.Union[int, float], unit: str = "", round_to_decimal_places: int = 3
) -> str:
    if not isinstance(number, (int, float)):
        raise TypeError("si_form() input number only accepts numbers (int or float)")
    if not isinstance(unit, str):
        raise TypeError("si_form() input unit only accepts strings")
    if not isinstance(round_to_decimal_places, int):
        raise TypeError("si_form() input round_to_decimal_places only accepts integers")

    if number == 0:
        mantissa_str = format(0.0, f".{round_to_decimal_places}f")
        return f"{mantissa_str} {unit}".strip()

    exponent = _get_engineering_exponent(number)
    mantissa_val = round(number / 10**exponent, round_to_decimal_places)

    # Core Bugfix 1: Check if formatting rounds the mantissa up to or past 1000 string representation
    if abs(round(mantissa_val, round_to_decimal_places)) >= 1000:
        exponent += 3
        mantissa_val = round(number / 10**exponent, round_to_decimal_places)

    # Core Bugfix 2: Fallback if exponent is missing OR if we are spilling outside dictionary limits
    prefix = _si_prefixes.get(exponent)
    if prefix is None and exponent != 0:
        return engineering_form(number, unit, round_to_decimal_places)

    # Catch boundary overflows (e.g., 10 * 10^60 is functionally 10^61, which is past 'QQ')
    if exponent == max(_si_prefixes.keys()) and abs(mantissa_val) >= 10:
        return engineering_form(number, unit, round_to_decimal_places)
    if exponent == min(_si_prefixes.keys()) and abs(mantissa_val) < 1:
        return engineering_form(number, unit, round_to_decimal_places)

    mantissa_str = format(mantissa_val, f".{round_to_decimal_places}f")
    outstr = f"{mantissa_str} {prefix}{unit}" if prefix is not None else f"{mantissa_str} {unit}"
    return outstr.strip()


def engineering_form(
    number: typing.Union[int, float], unit: str = "", round_to_decimal_places: int = 3
) -> str:
    if not isinstance(number, (int, float)):
        raise TypeError("engineering_form() input number only accepts numbers (int or float)")
    if not isinstance(unit, str):
        raise TypeError("engineering_form() input unit only accepts strings")
    if not isinstance(round_to_decimal_places, int):
        raise TypeError("engineering_form() input round_to_decimal_places only accepts integers")

    if number == 0:
        mantissa_str = format(0.0, f".{round_to_decimal_places}f")
        return f"{mantissa_str} {unit}".strip() if unit != "" else mantissa_str

    exponent = _get_engineering_exponent(number)
    mantissa_val = round(number / 10**exponent, round_to_decimal_places)

    if abs(round(mantissa_val, round_to_decimal_places)) >= 1000:
        exponent += 3
        mantissa_val = round(number / 10**exponent, round_to_decimal_places)

    mantissa_str = format(mantissa_val, f".{round_to_decimal_places}f")
    exp_str = _get_exp_str(exponent)
    return f"{mantissa_str}{exp_str} {unit}".strip() if unit != "" else f"{mantissa_str}{exp_str}"


def sif(num: float, uni: str = '', prec: int = 3) -> str:
    if not isinstance(num, (int, float)):
        raise TypeError('sif() only accepts numbers')
    return si_form(num, unit=uni, round_to_decimal_places=prec)


def engf(num: float, uni: str = '', prec: int = 3) -> str:
    if not isinstance(num, (int, float)):
        raise TypeError('engf() only accepts numbers')
    return engineering_form(num, unit=uni, round_to_decimal_places=prec)


def _test():
    test_cases = [
        (15050.504, 'V', 3),
        (389452.983745, 'V', 2),
        (0.0, 'A', 3),
        (-0.00000000001, 'A', 3),
        (-5432.1, 'Hz', 1),
        (1.23456, 'm', 1),
        (1.23456, 'm', 0),
        (1000, 'V', 0),
        (1000, 'V', 1),
        (1000, 'V', 2),
        (999.9, 'V', 0),
        (999.9, 'V', 1),
        (999.9, 'V', 2),
        (999.9, 'V', 3),
        (999.99, 'V', 0),
        (999.99, 'V', 1),
        (999.99, 'V', 2),
        (999.99, 'V', 3),
        (-999.9, 'V', 0),
        (-999.9, 'V', 1),
        (-999.9, 'V', 2),
        (-999.9, 'V', 3),
        (-999.99, 'V', 0),
        (-999.99, 'V', 1),
        (-999.99, 'V', 2),
        (-999.99, 'V', 3),
        (0.9999, 'A', 1),
        (0.99999, 'A', 3),
        (0.0009999, 'A', 3),
        (1e60, 'g', 3),
        (1e61, 'g', 3),
        (1e-60, 's', 3),
        (1e-61, 's', 3),
        (0.0055, 'F', 4),
        (-123456789, 'W', 2),
        (5.5e18, 'm/s', 1),
    ]

    print(f"{'Input Value':<15} | {'Unit':<5} | {'Decimals':<4} | {'SI Output':<20} | {'Engineering Output':<20}")
    print("-" * 75)

    for value, unit, prec in test_cases:
        res_si = si_form(value, unit, round_to_decimal_places=prec)
        res_eng = engineering_form(value, unit, round_to_decimal_places=prec)

        print(f"{value:<15g} | {unit:<5} | {prec:<4}     | {res_si:<20} | {res_eng:<20}")

    print("-" * 75)
    print("Test execution complete.")


if __name__ == '__main__':
    try:
        _test()
    except Exception as e:
        raise e
