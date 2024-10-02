import hmac
import time
import math
import base64


def generate_totp(secret, digits=6, period=30, algorithm='SHA1'):
    """
    Generate a Time-based One-Time Password (TOTP).

    Args:
        secret (str): The shared secret key.
        digits (int): The number of digits in the OTP.
        period (int): The time period in seconds for which the OTP is valid.
        algorithm (str): The hash algorithm to use (default is 'SHA1').

    Returns:
        str: The generated TOTP as a string of digits.
    """
    steps = math.floor(time.time() / period).to_bytes(8, 'big')
    hash_digest = hmac.digest(secret.encode(), steps, algorithm)

    offset = hash_digest[-1] & 0xf
    binary = (
        ((hash_digest[offset] & 0x7f) << 24) |
        ((hash_digest[offset + 1] & 0xff) << 16) |
        ((hash_digest[offset + 2] & 0xff) << 8) |
        (hash_digest[offset + 3] & 0xff)
    )
    return str(binary % 10**digits).rjust(digits, '0')


def generate_totp_url(secret, issuer, user, algorithm='SHA1', digits=6, period=30):
    """
    Generate a URL for a TOTP, which can be used to create a QR code for easy setup.

    Args:
        secret (str): The shared secret key.
        issuer (str): The issuer name (e.g., the service name).
        user (str): The username or identifier.
        algorithm (str): The hash algorithm to use (default is 'SHA1').
        digits (int): The number of digits in the OTP.
        period (int): The time period in seconds for which the OTP is valid.

    Returns:
        str: The URL for the TOTP.
    """
    b32_encoded_secret = base64.b32encode(secret.encode()).decode().rstrip('=')
    return (
        f"otpauth://totp/{issuer}:{user}"
        f"?secret={b32_encoded_secret}"
        f"&issuer={issuer}"
        f"&algorithm={algorithm}"
        f"&digits={digits}"
        f"&period={period}"
    )


# Example
print(
    generate_totp(
        secret='SuperDuper!#123!#1231',
        digits=6,
        period=30,
    )
)

print(
    generate_totp_url(
        secret='SuperDuper!#123!#1231',
        issuer='BasselTech Test',
        user='Bassel Admin',
        digits=6,
        period=30,
    )
)