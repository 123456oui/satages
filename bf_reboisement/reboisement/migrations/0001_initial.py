# Generated by Django 5.1.1 on 2024-09-16 12:17

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Acteur",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("nom", models.CharField(max_length=100)),
                ("prenom", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("mdp", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Carousel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="carousel_images/")),
                ("title", models.CharField(blank=True, max_length=200, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="Infos",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("info", models.TextField()),
                ("cree_le", models.DateTimeField(auto_now_add=True)),
                ("modifier_le", models.DateTimeField(auto_now=True)),
                ("valable_jusque", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="Materiel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("nom", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Partenaire",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("nom", models.CharField(max_length=100)),
                ("mail", models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Plante",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("nom_courant", models.CharField(max_length=100)),
                ("nom_scientifique", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Structure",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("nom", models.CharField(max_length=100)),
                ("mail", models.EmailField(max_length=254, unique=True)),
                ("logo", models.ImageField(upload_to="media/")),
            ],
        ),
        migrations.CreateModel(
            name="TypeLocalite",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("type", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="TypePlante",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("type_plante", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="TypeStructure",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("type_structure", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Activite",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("date", models.DateTimeField()),
                ("nb_plante", models.IntegerField()),
                ("nb_participant", models.IntegerField()),
                ("creer_le", models.DateTimeField(auto_now_add=True)),
                ("modifier_le", models.DateTimeField(auto_now=True)),
                ("statut", models.BooleanField(default=False)),
                (
                    "acteur",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reboisement.acteur",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Localite",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("nom_localite", models.CharField(max_length=100)),
                ("centrage", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reboisement.localite",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reboisement.typelocalite",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LocalitePolygone",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
                ),
                (
                    "localite",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reboisement.localite",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ActiviteMateriel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("nombre", models.IntegerField()),
                (
                    "activite",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reboisement.activite",
                    ),
                ),
                (
                    "materiel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reboisement.materiel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Media",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("file", models.FileField(upload_to="media/")),
                ("creer_le", models.DateTimeField(auto_now_add=True)),
                ("modifier_le", models.DateTimeField(auto_now=True)),
                (
                    "activite",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reboisement.activite",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Plants",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("nombre", models.IntegerField()),
                (
                    "activite",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reboisement.activite",
                    ),
                ),
                (
                    "plante",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reboisement.plante",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Site",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "polygone",
                    django.contrib.gis.db.models.fields.PolygonField(srid=4326),
                ),
                ("centrage", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                (
                    "activite",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reboisement.activite",
                    ),
                ),
                (
                    "localite",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reboisement.localite",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SourceFinance",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("montant", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "activite",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reboisement.activite",
                    ),
                ),
                (
                    "partenaire",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reboisement.partenaire",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PersonnelStructure",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "acteur",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reboisement.acteur",
                    ),
                ),
                (
                    "structure",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reboisement.structure",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="plante",
            name="type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="reboisement.typeplante"
            ),
        ),
        migrations.AddField(
            model_name="structure",
            name="type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="reboisement.typestructure",
            ),
        ),
    ]
