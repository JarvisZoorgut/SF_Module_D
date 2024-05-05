from django import template

register = template.Library()

STOP_LIST_WORDS = ['сосала', 'валят', 'отстой']

@register.filter()
def censor(value):
    stop_list = STOP_LIST_WORDS
    for word in value.split():
        if word.lower() in stop_list:
            value = value.replace(word, f'{word[0]}{"*" * (len(word)-1)}')
    return value
