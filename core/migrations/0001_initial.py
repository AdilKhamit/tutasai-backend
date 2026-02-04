from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=255)),
                ("role", models.CharField(choices=[("inspector", "Inspector"), ("lab_chief", "Lab Chief"), ("expert", "Expert"), ("committee", "Committee"), ("client", "Client")], max_length=20)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("password_hash", models.CharField(max_length=255)),
                ("digital_signature_key", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="Contract",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("contract_number", models.CharField(max_length=100)),
                ("project_name", models.CharField(max_length=255)),
                ("status", models.CharField(choices=[("active", "Активен"), ("completed", "Завершен")], max_length=20)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField(blank=True, null=True)),
                ("planned_inspection_date", models.DateField(blank=True, null=True)),
                ("client", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="contracts", to="core.user")),
            ],
        ),
        migrations.CreateModel(
            name="Object",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("location_name", models.CharField(max_length=255)),
                ("geo_coordinates", models.CharField(blank=True, max_length=100)),
                ("inv_number", models.CharField(blank=True, max_length=100)),
                ("serial_number", models.CharField(blank=True, max_length=100)),
                ("contract", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="objects", to="core.contract")),
            ],
        ),
        migrations.CreateModel(
            name="Qualification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("doc_type", models.CharField(choices=[("certificate", "Сертификат"), ("license", "Удостоверение"), ("lab_attestation", "Аттестат лаборатории")], max_length=50)),
                ("doc_number", models.CharField(max_length=100)),
                ("expiry_date", models.DateField()),
                ("scan_url", models.URLField(blank=True)),
                ("methods", models.CharField(blank=True, max_length=255)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="qualifications", to="core.user")),
            ],
        ),
        migrations.CreateModel(
            name="AccessLetter",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("generated_date", models.DateField()),
                ("file_url", models.URLField(blank=True)),
                ("contract", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="access_letters", to="core.contract")),
                ("inspectors", models.ManyToManyField(related_name="access_letters", to="core.user")),
            ],
        ),
        migrations.CreateModel(
            name="WorkCard",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("conditions_temp", models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ("conditions_humidity", models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ("conditions_light", models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ("raw_data_json", models.JSONField(blank=True, default=dict)),
                ("status", models.CharField(choices=[("draft", "Draft"), ("completed", "Completed")], default="draft", max_length=20)),
                ("inspector", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="work_cards", to="core.user")),
                ("object", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="work_cards", to="core.object")),
            ],
        ),
        migrations.CreateModel(
            name="Protocol",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("generated_content", models.JSONField(blank=True, default=dict)),
                ("inspector_signature", models.TextField(blank=True)),
                ("lab_chief_signature", models.TextField(blank=True)),
                ("lab_chief_status", models.CharField(choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")], default="pending", max_length=20)),
                ("rejection_reason", models.TextField(blank=True)),
                ("final_pdf_url", models.URLField(blank=True)),
                ("work_card", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="protocol", to="core.workcard")),
            ],
        ),
        migrations.CreateModel(
            name="AIAnalysis",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("risk_score", models.PositiveIntegerField()),
                ("forecast_text", models.TextField()),
                ("safety_status", models.CharField(choices=[("red", "Red"), ("yellow", "Yellow"), ("green", "Green")], max_length=10)),
                ("sent_to_committee", models.BooleanField(default=False)),
                ("protocol", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="ai_analysis", to="core.protocol")),
            ],
        ),
        migrations.CreateModel(
            name="ExpertConclusion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("conclusion_text", models.TextField()),
                ("expert_signature", models.TextField(blank=True)),
                ("full_package_url", models.URLField(blank=True)),
                ("expert", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="expert_conclusions", to="core.user")),
                ("protocol", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="expert_conclusions", to="core.protocol")),
            ],
        ),
    ]
