import uuid

import django.utils.timezone
from django.db import migrations, models


def completar_datos_encargos(apps, schema_editor):
    Encargo = apps.get_model('pasteleria', 'encargo')
    db_alias = schema_editor.connection.alias

    encargos = Encargo.objects.using(db_alias).select_related('producto')
    for encargo in encargos.iterator():
        encargo.codigo = uuid.uuid4()
        encargo.precio_unitario = encargo.producto.precio
        encargo.save(
            using=db_alias,
            update_fields=['codigo', 'precio_unitario'],
        )


class Migration(migrations.Migration):

    dependencies = [
        ('pasteleria', '0003_encargo_fecha_retiro'),
    ]

    operations = [
        migrations.AddField(
            model_name='encargo',
            name='cantidad',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='encargo',
            name='codigo',
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='encargo',
            name='creado',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='encargo',
            name='precio_unitario',
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10,
            ),
        ),
        migrations.RunPython(
            completar_datos_encargos,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name='encargo',
            name='codigo',
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name='encargo',
            name='creado',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
