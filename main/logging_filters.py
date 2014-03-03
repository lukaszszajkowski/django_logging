__author__ = 'Lukasz'

import json
import logging
l = logging.getLogger(__name__)

from inspect import stack, getmodule


from django_requestlogging.logging_filters import RequestFilter


class IncludeTeamFilter(logging.Filter):

    def __init__(self, teams=None):
        self.teams = teams

    def filter(self, record):
        record.filter_team = self.teams
        return True

class ExtendedRequestFilter(RequestFilter):

    def __init__(self, request=None):
        self.request = request

    def get_current_view(self):
        tmp_stack = stack()
        current_view  = '-'
        for line in tmp_stack:
            if "view" in line[1]:
                name = getmodule(line[0]).__name__
                current_view = "%s.%s" %(name, line[3])
        return current_view

    def check_if_filter_out(self, record):
        if hasattr(record, 'filter_team') and record.filter_team and record.team != '-':
            if record.team not in record.filter_team.split(","):
                return False
        return True

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

        record.current_view = self.get_current_view()

        if not self.check_if_filter_out(record):
            return False

        return super(ExtendedRequestFilter, self).filter(record)
