from __future__ import absolute_import

from functools import wraps

from django.http import HttpRequest

from django_ratelimit import ALL, UNSAFE
from django_ratelimit.exceptions import Ratelimited
from django_ratelimit.utils import is_django_ratelimited


__all__ = ['django_ratelimit']


def django_ratelimit(group=None, key=None, rate=None, method=ALL, block=False):
    def decorator(fn):
        @wraps(fn)
        def _wrapped(*args, **kw):
            # Work as a CBV method decorator.
            if isinstance(args[0], HttpRequest):
                request = args[0]
            else:
                request = args[1]
            request.limited = getattr(request, 'limited', False)
            django_ratelimited = is_django_ratelimited(request=request, group=group, fn=fn,
                                         key=key, rate=rate, method=method,
                                         increment=True)
            if django_ratelimited and block:
                raise Ratelimited()
            return fn(*args, **kw)
        return _wrapped
    return decorator


django_ratelimit.ALL = ALL
django_ratelimit.UNSAFE = UNSAFE
