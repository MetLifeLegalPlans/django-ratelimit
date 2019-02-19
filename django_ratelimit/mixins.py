from __future__ import absolute_import

from django_ratelimit import ALL, UNSAFE
from django_ratelimit.decorators import django_ratelimit


__all__ = ['RatelimitMixin']


class RatelimitMixin(object):
    """
    Mixin for usage in Class Based Views
    configured with the decorator ``django_ratelimit`` defaults.

    Configure the class-attributes prefixed with ``django_ratelimit_``
    for customization of the django_ratelimit process.

    Example::

        class ContactView(RatelimitMixin, FormView):
            form_class = ContactForm
            template_name = "contact.html"

            # Limit contact form by remote address.
            django_ratelimit_key = 'ip'
            django_ratelimit_block = True

            def form_valid(self, form):
                # Whatever validation.
                return super(ContactView, self).form_valid(form)

    """
    django_ratelimit_group = None
    django_ratelimit_key = None
    django_ratelimit_rate = '5/m'
    django_ratelimit_block = False
    django_ratelimit_method = ALL

    ALL = ALL
    UNSAFE = UNSAFE

    def get_django_ratelimit_config(self):
        # Ensures that the django_ratelimit_key is called as a function instead
        # of a method if it is a callable (ie self is not passed).
        if callable(self.django_ratelimit_key):
            self.django_ratelimit_key = self.django_ratelimit_key.__func__
        return dict(
            group=self.django_ratelimit_group,
            key=self.django_ratelimit_key,
            rate=self.django_ratelimit_rate,
            block=self.django_ratelimit_block,
            method=self.django_ratelimit_method,
        )

    def dispatch(self, *args, **kwargs):
        return django_ratelimit(
            **self.get_django_ratelimit_config()
        )(super(RatelimitMixin, self).dispatch)(*args, **kwargs)
