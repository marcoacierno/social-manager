# Generated by Django 2.1.2 on 2018-10-16 23:56

from django.db import migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_metadata_payload'),
    ]

    operations = [
        migrations.AddField(
            model_name='metadata',
            name='status',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], default='created', max_length=100, no_check_for_status=True, verbose_name='status'),
        ),
        migrations.AddField(
            model_name='metadata',
            name='status_changed',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', verbose_name='status changed'),
        ),
        migrations.AlterUniqueTogether(
            name='metadata',
            unique_together={('post', 'provider_name')},
        ),
    ]