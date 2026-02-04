from django.utils import timezone
from rest_framework import routers, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from core import models, serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class QualificationViewSet(viewsets.ModelViewSet):
    queryset = models.Qualification.objects.all()
    serializer_class = serializers.QualificationSerializer


class ContractViewSet(viewsets.ModelViewSet):
    queryset = models.Contract.objects.all()
    serializer_class = serializers.ContractSerializer


class ObjectViewSet(viewsets.ModelViewSet):
    queryset = models.Object.objects.all()
    serializer_class = serializers.ObjectSerializer


class AccessLetterViewSet(viewsets.ModelViewSet):
    queryset = models.AccessLetter.objects.all()
    serializer_class = serializers.AccessLetterSerializer


class WorkCardViewSet(viewsets.ModelViewSet):
    queryset = models.WorkCard.objects.all()
    serializer_class = serializers.WorkCardSerializer


class ProtocolViewSet(viewsets.ModelViewSet):
    queryset = models.Protocol.objects.all()
    serializer_class = serializers.ProtocolSerializer


class AIAnalysisViewSet(viewsets.ModelViewSet):
    queryset = models.AIAnalysis.objects.all()
    serializer_class = serializers.AIAnalysisSerializer


class ExpertConclusionViewSet(viewsets.ModelViewSet):
    queryset = models.ExpertConclusion.objects.all()
    serializer_class = serializers.ExpertConclusionSerializer


class CommitteeDashboardView(APIView):
    def get(self, request):
        today = timezone.now().date()
        data = []
        for obj in models.Object.objects.select_related("contract").all():
            contract = obj.contract
            protocol = getattr(obj.work_cards.order_by("-created_at").first(), "protocol", None)
            status = "unknown"
            if not protocol:
                if contract.planned_inspection_date and today > contract.planned_inspection_date:
                    status = "red"
            else:
                analysis = getattr(protocol, "ai_analysis", None)
                if analysis:
                    status = analysis.safety_status
            data.append(
                {
                    "object_id": obj.id,
                    "object_name": obj.name,
                    "contract_id": contract.id,
                    "planned_inspection_date": contract.planned_inspection_date,
                    "status": status,
                }
            )
        return Response(data)


router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"qualifications", QualificationViewSet)
router.register(r"contracts", ContractViewSet)
router.register(r"objects", ObjectViewSet)
router.register(r"access-letters", AccessLetterViewSet)
router.register(r"work-cards", WorkCardViewSet)
router.register(r"protocols", ProtocolViewSet)
router.register(r"ai-analysis", AIAnalysisViewSet)
router.register(r"expert-conclusions", ExpertConclusionViewSet)
