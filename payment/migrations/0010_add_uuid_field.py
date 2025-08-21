import uuid
from django.db import migrations, models


def generate_uuids(apps, schema_editor):
    Order = apps.get_model('payment', 'Order')
    for order in Order.objects.all():
        order.uuid = uuid.uuid4()
        order.save(update_fields=['uuid'])


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0009_alter_order_last_update_alter_order_shipping_address"),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, unique=False),
        ),
        migrations.RunPython(generate_uuids),
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
