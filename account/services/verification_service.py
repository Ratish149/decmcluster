import logging

from django.contrib.auth import get_user_model
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner

logger = logging.getLogger(__name__)
User = get_user_model()

# Cryptographic signer with custom salt for email verification
signer = TimestampSigner(salt="email-verification")


def generate_verification_token(user) -> str:
    """
    Generates a secure, signed token for the user.
    """
    return signer.sign(str(user.id))


def verify_token_and_get_user(token: str, max_age: int = 86400):
    """
    Unsigns the token, validates its age, and returns the corresponding User.
    Returns None if verification fails (expired or invalid signature).
    """
    try:
        user_id = signer.unsign(token, max_age=max_age)
        return User.objects.filter(id=user_id).first()
    except SignatureExpired:
        logger.warning("Email verification token has expired.")
    except BadSignature:
        logger.warning("Invalid signature on email verification token.")
    except Exception as e:
        logger.error(f"Unexpected error during token verification: {e}")
    return None
