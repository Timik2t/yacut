import re
import string

VALID_CHARS = string.ascii_letters + string.digits
SHORT_PATTERN = r'^[' + re.escape(VALID_CHARS) + r']+$'

DEFAULT_SHORT_LENGTH = 6
MAX_SHORT_LENGTH = 16
ORIGINAL_LENGTH = 512

REDIRECT_URL_MAP = 'redirect_to_url'

MAX_ATTEMPTS = 100
