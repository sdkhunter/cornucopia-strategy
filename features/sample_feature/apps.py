from django.apps import AppConfig

class SampleFeatureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'features.sample_feature'
    verbose_name = "Sample Feature"
