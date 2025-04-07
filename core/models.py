from django.db import models
from django.utils import timezone
import pytz

class TblFormDataNew(models.Model):
    subscription_date = models.DateTimeField()
    cta_url = models.CharField(max_length=255, blank=True)
    cta_source = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=100, blank=True)  # 🔧 Added blank=True
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    refid = models.CharField(max_length=100, blank=True)
    tagid = models.CharField(max_length=100, blank=True)
    subscriber_password = models.CharField(max_length=255, blank=True)
    subscriber_group = models.CharField(max_length=100, blank=True)
    personality_prefix = models.CharField(max_length=50, blank=True)
    shares = models.CharField(max_length=10, default="0")
    credits = models.CharField(max_length=10, default="0")
    decoding_requests = models.CharField(max_length=10, default="0")
    total_submissions = models.CharField(max_length=10, default="0")

    def __str__(self):
        return self.email

    @property
    def pacific_time(self):
        if self.subscription_date:
            pst = pytz.timezone("US/Pacific")
            aware = self.subscription_date
            if timezone.is_naive(aware):
                aware = timezone.make_aware(aware)
            return aware.astimezone(pst).strftime("%b. %d, %Y, %I:%M %p")
        return ""

class FeatureToggle(models.Model):
    feature_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.feature_name

from django.db import models

class FetchLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    script_name = models.CharField(max_length=100)
    success = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {self.script_name}"


