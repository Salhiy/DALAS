import re
import os
from datetime import datetime
from time import mktime


def format_string(s):
	return re.sub(r"\s", "", re.sub(r"[^\d.-]", "", s))

def get_abs_path(path):
	return os.path.abspath(path).replace("\\", "/")

def convert_to_unix(date):
	datum = datetime.strptime(date, '%d-%m-%Y')
	return int(mktime(datum.timetuple()))