__author__ = 'Lukasz'

import logging
l = logging.getLogger(__name__)
from django.http import HttpResponse, HttpResponseRedirect

from functools import wraps
def tas_view_audit(operation_label="VIEW", resource_lable=None, log_level=logging.INFO, request_method=None):
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            responce = func(request, *args, **kwargs)
            if not request_method or request_method == request.method:
                msg = "%s: function %s with parameters %s" %(operation_label, func.__name__, str(*args))
                l.log(log_level, msg)
            return responce
        return wraps(func)(inner_decorator)
    return decorator

def tas_audit(operation_label="VIEW", resource_lable=None, log_level=logging.INFO):
    def wrap(func):
        def wrapped_f(*args):
            func(*args)
            msg = "%s: function %s with parameters %s" %(operation_label, func.__name__, str(*args))
            l.log(log_level, msg)
            return wrapped_f
    return wrap
