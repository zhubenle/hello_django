import re

PT_USERNAME = re.compile(r'[a-zA-Z0-9_]{8,20}')
PT_PASSWORD = re.compile(r'\S{8,32}')
PT_REAL_NAME = re.compile(r'\S{2,}')
PT_PHONE = re.compile(r'^1[34578]\d{9}$')
PT_EMAIL = re.compile(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')

PT_ROLE_NAME = re.compile(r'[A-Z0-9_]{3,32}')

PT_MENU_TITLE = re.compile(r'\S{2,64}')
PT_MENU_URL = re.compile(r'\S{4,200}')
