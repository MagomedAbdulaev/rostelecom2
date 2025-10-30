from django import template

register = template.Library()

@register.filter
def in_list(value, arg):
    """Проверяет, содержится ли значение в списке"""
    if value and arg in value:
        return True
    return False