from modeltranslation.translator import TranslationOptions, register

from .models import WorkerProfile


@register(WorkerProfile)
class WorkerProfileTranslationOptions(TranslationOptions):
    fields = ('fullname', 'description')

