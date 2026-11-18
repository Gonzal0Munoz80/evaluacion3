import django.db.models.deletion
from django.db import migrations, models


def asignar_linea_a_productos_existentes(apps, schema_editor):
    Linea = apps.get_model('pasteleria', 'linea')
    Producto = apps.get_model('pasteleria', 'producto')
    db_alias = schema_editor.connection.alias

    linea_sin_clasificar, _ = Linea.objects.using(db_alias).get_or_create(
        nombre='Sin clasificar',
    )
    Producto.objects.using(db_alias).filter(linea__isnull=True).update(
        linea_id=linea_sin_clasificar.pk,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('pasteleria', '0005_producto_visible_en_catalogo'),
    ]

    operations = [
        migrations.CreateModel(
            name='linea',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='linea',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='productos',
                to='pasteleria.linea',
            ),
        ),
        migrations.AddField(
            model_name='producto',
            name='apto_celiacos',
            field=models.BooleanField(
                default=False,
                verbose_name='Apto para celíacos',
            ),
        ),
        migrations.RunPython(
            asignar_linea_a_productos_existentes,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name='producto',
            name='linea',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='productos',
                to='pasteleria.linea',
            ),
        ),
    ]
