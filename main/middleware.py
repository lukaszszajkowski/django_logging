__author__ = 'Lukasz'
import logging

from django_requestlogging.middleware import LogSetupMiddleware
from .logging_filters import ExtendedRequestFilter

class LogRequestMiddleware(LogSetupMiddleware):
    FILTER = ExtendedRequestFilter

    def find_loggers(self):
        """
        Returns a :class:`dict` of names and the associated loggers.
        """
        # Extract the full logger tree from Logger.manager.loggerDict
        # that are under ``self.root``.
        result = {}
        prefix = self.root + '.'
        for name, logger in logging.Logger.manager.loggerDict.items():
            if self.root and not name.startswith(prefix):
                # Does not fall under self.root
                continue
            result[name] = logger
        # Add the self.root logger
        result[self.root] = logging.getLogger(self.root)
        return result


    def process_request(self, request):
        """Adds a filter, bound to *request*, to the appropriate loggers."""
        request.logging_filter = ExtendedRequestFilter(request)
        self.add_filter(request.logging_filter)
