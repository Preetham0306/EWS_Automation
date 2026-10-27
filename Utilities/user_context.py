import threading

_context = threading.local()

def set_user_ip(ip):
    _context.user_ip = ip

def get_user_ip():
    return getattr(_context, "user_ip", "")