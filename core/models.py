from django.db import models


class UserRole(models.TextChoices):
    INSPECTOR = "inspector", "Inspector"
    LAB_CHIEF = "lab_chief", "Lab Chief"
    EXPERT = "expert", "Expert"
    COMMITTEE = "committee", "Committee"
    CLIENT = "client", "Client"


class User(models.Model):
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=UserRole.choices)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    digital_signature_key = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.full_name} ({self.role})"


class Qualification(models.Model):
    DOC_TYPES = [
        ("certificate", "Сертификат"),
        ("license", "Удостоверение"),
        ("lab_attestation", "Аттестат лаборатории"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="qualifications")
    doc_type = models.CharField(max_length=50, choices=DOC_TYPES)
    doc_number = models.CharField(max_length=100)
    expiry_date = models.DateField()
    scan_url = models.URLField(blank=True)
    methods = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return f"{self.get_doc_type_display()} {self.doc_number}"


class ContractStatus(models.TextChoices):
    ACTIVE = "active", "Активен"
    COMPLETED = "completed", "Завершен"


class Contract(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contracts")
    contract_number = models.CharField(max_length=100)
    project_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=ContractStatus.choices)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    planned_inspection_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.contract_number} - {self.project_name}"


class Object(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="objects")
    name = models.CharField(max_length=255)
    location_name = models.CharField(max_length=255)
    geo_coordinates = models.CharField(max_length=100, blank=True)
    inv_number = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.name


class AccessLetter(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="access_letters")
    inspectors = models.ManyToManyField(User, related_name="access_letters")
    generated_date = models.DateField()
    file_url = models.URLField(blank=True)

    def __str__(self) -> str:
        return f"Access letter {self.id}"


class WorkCardStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    COMPLETED = "completed", "Completed"


class WorkCard(models.Model):
    inspector = models.ForeignKey(User, on_delete=models.CASCADE, related_name="work_cards")
    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name="work_cards")
    created_at = models.DateTimeField(auto_now_add=True)
    conditions_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    conditions_humidity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    conditions_light = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    raw_data_json = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=WorkCardStatus.choices, default=WorkCardStatus.DRAFT)

    def __str__(self) -> str:
        return f"Work card {self.id}"


class LabChiefStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"


class Protocol(models.Model):
    work_card = models.OneToOneField(WorkCard, on_delete=models.CASCADE, related_name="protocol")
    generated_content = models.JSONField(default=dict, blank=True)
    manual_content = models.JSONField(default=dict, blank=True)
    generation_method = models.CharField(
        max_length=20,
        choices=[("ai", "AI"), ("manual", "Manual")],
        default="manual",
    )
    draft_text = models.TextField(blank=True)
    inspector_signature = models.TextField(blank=True)
    lab_chief_signature = models.TextField(blank=True)
    lab_chief_status = models.CharField(
        max_length=20,
        choices=LabChiefStatus.choices,
        default=LabChiefStatus.PENDING,
    )
    rejection_reason = models.TextField(blank=True)
    final_pdf_url = models.URLField(blank=True)
    nca_layer_transaction_id = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return f"Protocol {self.id}"


class SafetyStatus(models.TextChoices):
    RED = "red", "Red"
    YELLOW = "yellow", "Yellow"
    GREEN = "green", "Green"


class AIAnalysis(models.Model):
    protocol = models.OneToOneField(Protocol, on_delete=models.CASCADE, related_name="ai_analysis")
    risk_score = models.PositiveIntegerField()
    forecast_text = models.TextField()
    safety_status = models.CharField(max_length=10, choices=SafetyStatus.choices)
    sent_to_committee = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"AI analysis {self.id}"


class ExpertConclusion(models.Model):
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE, related_name="expert_conclusions")
    expert = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expert_conclusions")
    conclusion_text = models.TextField()
    expert_signature = models.TextField(blank=True)
    full_package_url = models.URLField(blank=True)

    def __str__(self) -> str:
        return f"Expert conclusion {self.id}"
