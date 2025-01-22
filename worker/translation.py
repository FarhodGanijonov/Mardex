from modeltranslation.translator import TranslationOptions, register

from .models import WorkerProfile, WorkerNews


@register(WorkerProfile)
class WorkerProfileTranslationOptions(TranslationOptions):
    fields = ('fullname', 'description')


@register(WorkerNews)
class WorkerNewsTranslationOptions(TranslationOptions):
    fields = ('description',)
