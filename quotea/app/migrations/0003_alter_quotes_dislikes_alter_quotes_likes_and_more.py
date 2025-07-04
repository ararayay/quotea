# Generated by Django 5.2.3 on 2025-07-01 19:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_weigth_quotes_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotes',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='quotes',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='quotes',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='quotes',
            name='weight',
            field=models.IntegerField(default=1),
        ),
        migrations.CreateModel(
            name='QuoteLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('type', models.CharField(choices=[('like', 'Like'), ('dislike', 'Dislike')], max_length=10)),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.quotes')),
            ],
            options={
                'unique_together': {('quote', 'ip_address')},
            },
        ),
    ]
