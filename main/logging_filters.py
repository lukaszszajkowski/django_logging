__author__ = 'Lukasz'

import json
import logging
from django_requestlogging.logging_filters import RequestFilter

class IncludeTeamFilter(logging.Filter):

    def __init__(self, teams, request=None):
        self.request = request
        self.teams = teams


    def filter(self, record):

        if hasattr(record, 'team'):
            if record.team not in self.teams.split(","):
                return False


        return True

class ExtendedRequestFilter(RequestFilter):

    def filter(self, record):
        request = self.request
        META = getattr(request, 'META', {})
        record.query_string = META.get('QUERY_STRING', '-')
        record.team = '-'
        if hasattr(request, 'session'):
            record.session_key = request.session.session_key
            record.team = request.session.get('team', 'guest_team')
        else:
            record.session_key = '-'

        if hasattr(request, 'method') and request.method == 'POST':
            record.post_string = json.dumps(request.POST)
        else:
            record.post_string = '-'

        return super(ExtendedRequestFilter, self).filter(record)