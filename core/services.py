from core import models


def generate_ai_protocol(work_card: models.WorkCard) -> dict:
    """Stub for AI-generated protocol content."""
    return {
        "summary": "AI-generated content placeholder",
        "work_card_id": work_card.id,
    }


def create_ai_analysis(protocol: models.Protocol) -> models.AIAnalysis:
    return models.AIAnalysis.objects.create(
        protocol=protocol,
        risk_score=0,
        forecast_text="",
        safety_status=models.SafetyStatus.GREEN,
        sent_to_committee=False,
    )
