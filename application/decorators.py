from flask import redirect, request, url_for
from functools import wraps

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if not ('uid' in request.cookies.keys() and request.cookies.get('uid') == '1'):
			return redirect(url_for('login'))
		return f(*args, **kwargs)
	return decorated_function