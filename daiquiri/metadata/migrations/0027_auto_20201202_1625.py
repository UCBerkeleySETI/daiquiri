# Generated by Django 2.2.17 on 2020-12-02 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daiquiri_metadata', '0026_add_creators_and_contributors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schema',
            name='license',
            field=models.CharField(blank=True, choices=[('CC0', 'CC0 1.0 Universal (CC0 1.0)'), ('PD', 'Public Domain Mark'), ('BY', 'Attribution 4.0 International (CC BY 4.0)'), ('BY_SA', 'Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)'), ('BY_ND', 'Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)'), ('BY_NC', 'Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)'), ('BY_NC_SA', 'Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)'), ('BY_NC_ND', 'Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)')], max_length=8, null=True, verbose_name='License'),
        ),
        migrations.AlterField(
            model_name='table',
            name='license',
            field=models.CharField(blank=True, choices=[('CC0', 'CC0 1.0 Universal (CC0 1.0)'), ('PD', 'Public Domain Mark'), ('BY', 'Attribution 4.0 International (CC BY 4.0)'), ('BY_SA', 'Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)'), ('BY_ND', 'Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)'), ('BY_NC', 'Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)'), ('BY_NC_SA', 'Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)'), ('BY_NC_ND', 'Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)')], max_length=8, null=True, verbose_name='License'),
        ),
    ]
