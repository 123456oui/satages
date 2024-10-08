# Generated by Django 5.1.1 on 2024-09-16 12:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reboisement", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activite",
            name="acteur",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="reboisement.acteur"
            ),
        ),
        migrations.AlterField(
            model_name="activitemateriel",
            name="activite",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="reboisement.activite",
            ),
        ),
        migrations.AlterField(
            model_name="activitemateriel",
            name="materiel",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="reboisement.materiel",
            ),
        ),
        migrations.AlterField(
            model_name="localite",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="reboisement.localite",
            ),
        ),
        migrations.AlterField(
            model_name="localite",
            name="type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="reboisement.typelocalite",
            ),
        ),
        migrations.AlterField(
            model_name="localitepolygone",
            name="localite",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="reboisement.localite",
            ),
        ),
        migrations.AlterField(
            model_name="media",
            name="activite",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="reboisement.activite",
            ),
        ),
        migrations.AlterField(
            model_name="personnelstructure",
            name="acteur",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="reboisement.acteur"
            ),
        ),
        migrations.AlterField(
            model_name="personnelstructure",
            name="structure",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="reboisement.structure",
            ),
        ),
        migrations.AlterField(
            model_name="plante",
            name="type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="reboisement.typeplante",
            ),
        ),
        migrations.AlterField(
            model_name="plants",
            name="activite",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="reboisement.activite",
            ),
        ),
        migrations.AlterField(
            model_name="plants",
            name="plante",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="reboisement.plante"
            ),
        ),
        migrations.AlterField(
            model_name="site",
            name="activite",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="reboisement.activite",
            ),
        ),
        migrations.AlterField(
            model_name="site",
            name="localite",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="reboisement.localite",
            ),
        ),
        migrations.AlterField(
            model_name="sourcefinance",
            name="activite",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="reboisement.activite",
            ),
        ),
        migrations.AlterField(
            model_name="sourcefinance",
            name="partenaire",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="reboisement.partenaire",
            ),
        ),
        migrations.AlterField(
            model_name="structure",
            name="type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="reboisement.typestructure",
            ),
        ),
    ]
