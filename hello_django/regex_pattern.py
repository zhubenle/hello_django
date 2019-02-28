import re

PT_PHONE = re.compile(r'\d{11}')
PT_EMAIL = re.compile(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')
