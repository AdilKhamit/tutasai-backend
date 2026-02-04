from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import routers, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from core import models, serializers, services


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


class InspectorDashboardView(APIView):
    def get(self, request):
        completed_cards = models.WorkCard.objects.filter(status=models.WorkCardStatus.COMPLETED)
        serializer = serializers.WorkCardSerializer(completed_cards, many=True)
        return Response(serializer.data)


class GenerateProtocolView(APIView):
    def post(self, request, work_card_id):
        work_card = get_object_or_404(models.WorkCard, id=work_card_id)
        generated_content = services.generate_ai_protocol(work_card)
        protocol = models.Protocol.objects.create(
            work_card=work_card,
            generated_content=generated_content,
            generation_method="ai",
        )
        serializer = serializers.ProtocolSerializer(protocol)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SignProtocolView(APIView):
    def post(self, request, protocol_id):
        protocol = get_object_or_404(models.Protocol, id=protocol_id)
        signature = request.data.get("signature")
        nca_layer_tx = request.data.get("nca_layer_transaction_id", "")
        if not signature:
            return Response(
                {"detail": "signature is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        protocol.inspector_signature = signature
        protocol.nca_layer_transaction_id = nca_layer_tx
        protocol.save(update_fields=["inspector_signature", "nca_layer_transaction_id"])
        return Response({"status": "signed"})


class CommitteeDashboardView(APIView):
    def get(self, request):
        today = timezone.now().date()
        data = []
        for obj in models.Object.objects.select_related("contract").all():
            contract = obj.contract
            latest_card = obj.work_cards.order_by("-created_at").first()
            protocol = getattr(latest_card, "protocol", None) if latest_card else None
            status_value = "unknown"
            if not protocol:
                if contract.planned_inspection_date and today > contract.planned_inspection_date:
                    status_value = "red"
            else:
                analysis = getattr(protocol, "ai_analysis", None)
                if analysis:
                    status_value = analysis.safety_status
            data.append(
                {
                    "object_id": obj.id,
                    "object_name": obj.name,
                    "contract_id": contract.id,
                    "planned_inspection_date": contract.planned_inspection_date,
                    "status": status_value,
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
