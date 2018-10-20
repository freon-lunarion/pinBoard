# Generated by Django 2.1.1 on 2018-10-20 10:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shared', '0004_auto_20181020_2112'),
        ('blogs', '0003_auto_20181020_1351'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfavorite',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='userfavorite',
            name='post',
        ),
        migrations.RemoveField(
            model_name='userfavorite',
            name='user',
        ),
        migrations.AddField(
            model_name='qnaquestion',
            name='is_pinned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='qnaquestion',
            name='operator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='qnaquestion',
            name='pin_board',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='shared.PinBoard'),
        ),
        migrations.DeleteModel(
            name='UserFavorite',
        ),
    ]