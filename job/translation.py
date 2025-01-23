from modeltranslation.translator import TranslationOptions, register

from .models import CategoryJob, Job, City, Region


@register(CategoryJob)
class CategoryJobTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Job)
class JobTranslationOptions(TranslationOptions):
    fields = ('title',)
