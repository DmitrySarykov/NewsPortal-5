from django import template
 
register = template.Library() 

@register.filter(name='censor')  
def censor(value):
    if isinstance(value, str):
        list = ['ух', 'ор', 'ах', 'ай'] # Список нецензурных слов
        for A in list:
            value = value.replace(A, '@%') # Замена совпадений подстроки на @!#%
        return str(value)
    else:
        raise ValueError(f'Нельзя преобразовать {type(value)}')
    