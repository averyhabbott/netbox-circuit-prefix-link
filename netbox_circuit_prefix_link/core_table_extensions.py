import django_tables2 as tables
from circuits.tables import CircuitTable
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from utilities.tables import register_table_column


class LinkedPrefixesColumn(tables.Column):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('verbose_name', _('Linked Prefixes'))
        kwargs.setdefault('accessor', tables.A('linked_prefixes'))
        kwargs.setdefault('orderable', False)
        super().__init__(*args, **kwargs)

    def render(self, value):
        links = value.select_related('prefix').all()
        if not links:
            return mark_safe('&mdash;')
        return format_html_join(
            mark_safe(', '),
            '<a href="{}">{}</a>',
            ((link.prefix.get_absolute_url(), str(link.prefix)) for link in links),
        )


register_table_column(LinkedPrefixesColumn(), 'linked_prefixes', CircuitTable)
