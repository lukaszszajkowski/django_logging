__author__ = 'Lukasz'
import os
from os.path import abspath, basename, dirname, join, normpath
DJANGO_ROOT = dirname(dirname(abspath(__file__)))


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(team)s %(path_info)s %(levelname)s  %(team)s %(username)s %(module)s %(message)s'
        },
        'request_format': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(remote_addr)s %(team)s %(username)s "%(request_method)s '
            '%(server_protocol)s" %(http_user_agent)s %(path_info)s '
            '%(message)s',
        },
        'request_extended_format': {
            'format': '%(levelname)s %(asctime)s %(module)s.%(funcName)s():%(lineno)d %(current_view)s %(process)d %(thread)d %(session_key)s %(remote_addr)s %(team)s %(username)s "%(request_method)s '
            '%(server_protocol)s" %(http_user_agent)s %(path_info)s %(query_string)s %(post_string)s '
            '%(message)s',
        },
    },
    'filters': {
        'include_teams': {
            '()': 'main.logging_filters.IncludeTeamFilter',
            'teams': 'my_team',
        },
        'request': {
            '()': 'main.logging_filters.ExtendedRequestFilter',
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['request'],
            'formatter': 'simple',
        },
        'console2':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            #'formatter': 'simple',
            'filters': ['request'],
            'formatter': 'request_format',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': []
        },
        'sql_file_info': {                # define and name a handler
            'level': 'DEBUG',
            'class': 'logging.FileHandler', # set the logging class to log to a file
            'filters': ['request'],
            'formatter': 'request_extended_format',         # define the formatter to associate
            'filename': os.path.join(DJANGO_ROOT, 'log', 'sql.log') # log file
        },
        'http_file_info': {                # define and name a handler
            'level': 'INFO',
            'class': 'logging.FileHandler', # set the logging class to log to a file
            'filters': ['request'],
            'formatter': 'request_extended_format', # define the formatter to associate
            'filename': os.path.join(DJANGO_ROOT, 'log', 'http.log') # log file
        },
        'project_file_info': {                # define and name a handler
            'level': 'DEBUG',
            'class': 'logging.FileHandler', # set the logging class to log to a file
            'formatter': 'verbose',         # define the formatter to associate
            'filename': os.path.join(DJANGO_ROOT, 'log', 'project.log') # log file
        },
        'audit_file_info': {                # define and name a handler
            'level': 'DEBUG',
            'class': 'logging.FileHandler', # set the logging class to log to a file
            'filters': ['request'],
            'formatter': 'request_extended_format',         # define the formatter to associate
            'filename': os.path.join(DJANGO_ROOT, 'log', 'audit.log') # log file
        },
    },
    'loggers': {
        'main.audit': {
            'handlers': ['console','audit_file_info'],
            'level': 'DEBUG',
            'propagate': True,
            'filters': []
        },
        'django': {
            'handlers': ['console','http_file_info'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console','http_file_info'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'main': {
            'handlers': ['console','project_file_info', 'http_file_info'],
            'level': 'INFO',
            'filters': []
        },

        'django.db.backends': {              # define a logger - give it a name
            'handlers': ['console','sql_file_info'], # specify what handler to associate
            'level': 'DEBUG',                 # specify the logging level
            'propagate': False,
        },
        # you can also shortcut 'loggers' and just configure logging for EVERYTHING at once
        #'root': {
        #    'handlers': ['console', 'project_file_info'],
        #    'level': 'DEBUG'
        #},
    }
}