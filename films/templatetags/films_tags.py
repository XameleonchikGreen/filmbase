from django import template
from django.apps import apps

register = template.Library()


@register.filter
def model_verbose_name(cls_name):
    Model = apps.get_model(*cls_name.split(":"))
    return Model._meta.verbose_name


@register.filter
def model_verbose_name_plural(cls_name):
    Model = apps.get_model(*cls_name.split(":"))
    return Model._meta.verbose_name_plural


@register.simple_tag
def verbose_name(obj, field):
    return obj._meta.get_field(field).verbose_name


@register.filter
def ru_plural(value, variants):
    variants = variants.split(",")
    value = abs(int(value))
    if value % 10 == 1 and value % 100 != 11:
        variant = 0
    elif value % 10 >= 2 and value % 10 <= 4 and \
            (value % 100 < 10 or value % 100 >= 20):
        variant = 1
    else:
        variant = 2
    return variants[variant]


@register.filter
def group_admin_or_superuser(user, group):
    memberships = user.membership_set.filter(group=group)
    if memberships.count() == 0:
        return user.is_superuser
    return user.is_superuser or memberships[0].is_admin


@register.filter
def not_in_group(user, group):
    memberships = user.membership_set.filter(group=group)
    return memberships.count() == 0


@register.filter
def group_waiter(user, group):
    memberships = user.membership_set.filter(group=group)
    return memberships.count() > 0 and memberships[0].is_waiter


@register.filter
def in_group_or_superuser(user, group):
    memberships = user.membership_set.filter(group=group)
    return (user.is_superuser or
            (memberships.count() > 0 and not memberships[0].is_waiter))
