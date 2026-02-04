from django.db.models.signals import post_save
from django.dispatch import receiver

from core import models


@receiver(post_save, sender=models.Protocol)
def ensure_ai_analysis(sender, instance: models.Protocol, created: bool, **kwargs):
    if not created:
        return
    if hasattr(instance, "ai_analysis"):
        return
    models.AIAnalysis.objects.create(
        protocol=instance,
        risk_score=0,
        forecast_text="",
        safety_status=models.SafetyStatus.GREEN,
        sent_to_committee=False,
    )
