from modeltranslation.translator import TranslationOptions, register
from .models import Order


@register(Order)
class OrderTranslationOptions(TranslationOptions):
    fields = ('desc', 'full_desc',)



