from django.utils import timezone
from rest_framework import serializers

from core import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"


class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Qualification
        fields = "__all__"


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contract
        fields = "__all__"


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Object
        fields = "__all__"


class AccessLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccessLetter
        fields = "__all__"


class WorkCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WorkCard
        fields = "__all__"

    def validate(self, attrs):
        status = attrs.get("status")
        if status == models.WorkCardStatus.COMPLETED:
            raw_data = attrs.get("raw_data_json")
            if not raw_data:
                raise serializers.ValidationError(
                    "Для завершенной рабочей карты требуется raw_data_json."
                )
        return attrs


class ProtocolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Protocol
        fields = "__all__"

    def validate(self, attrs):
        generation_method = attrs.get("generation_method")
        if generation_method == "ai" and not attrs.get("generated_content"):
            raise serializers.ValidationError(
                "Для AI-генерации требуется заполненный generated_content."
            )
        if generation_method == "manual" and not attrs.get("manual_content"):
            raise serializers.ValidationError(
                "Для ручного заполнения требуется manual_content."
            )
        work_card = attrs.get("work_card")
        if work_card:
            inspector = work_card.inspector
            today = timezone.now().date()
            is_valid = inspector.qualifications.filter(expiry_date__gte=today).exists()
            if not is_valid:
                raise serializers.ValidationError(
                    "У инспектора нет действующей квалификации. "
                    "Создание протокола запрещено."
                )
        return attrs


class AIAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AIAnalysis
        fields = "__all__"


class ExpertConclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExpertConclusion
        fields = "__all__"
