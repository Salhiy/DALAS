import re

def format_string(s):
	return re.sub(r"\s", "", re.sub(r"[^\d.-]", "", s))