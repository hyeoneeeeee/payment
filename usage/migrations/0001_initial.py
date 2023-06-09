# Generated by Django 4.1.3 on 2023-03-31 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Usage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True, verbose_name='사용시작 시간')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='사용종료 시간')),
                ('usage_time', models.TextField(blank=True, null=True, verbose_name='사용한 시간')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='사용유저')),
            ],
        ),
    ]
