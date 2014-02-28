__author__ = 'Lukasz'
import logging

from django_requestlogging.middleware import LogSetupMiddleware
from .logging_filters import ExtendedRequestFilter

class LogRequestMiddleware(LogSetupMiddleware):
    FILTER = ExtendedRequestFilter

    def ooo_find_filterer_with_filter(self, filterers, filter_cls):
        """
        Returns a :class:`dict` of filterers mapped to a list of filters.

        *filterers* should be a list of filterers.

        *filter_cls* should be a logging filter that should be matched.
        """
        result = {}
        for logger in filterers:
            filters = [f for f in getattr(logger, 'filters', [])
                       if isinstance(f, filter_cls)]
            if filters:
                result[logger] = filters
        return result

    def aaaadd_filter(self, f, filter_cls=None):
        """Add filter *f* to any loggers that have *filter_cls* filters."""
        if filter_cls is None:
            filter_cls = type(f)
        for logger in self.find_loggers_with_filter(filter_cls):
            logger.addFilter(f)
        for handler in self.find_handlers_with_filter(filter_cls):
            handler.addFilter(f)

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
