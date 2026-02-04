from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="protocol",
            name="draft_text",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="protocol",
            name="generation_method",
            field=models.CharField(choices=[("ai", "AI"), ("manual", "Manual")], default="manual", max_length=20),
        ),
        migrations.AddField(
            model_name="protocol",
            name="manual_content",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name="protocol",
            name="nca_layer_transaction_id",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
