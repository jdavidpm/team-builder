# Generated by Django 3.1.7 on 2021-05-25 22:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0013_profile_results_private'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='evaluation_p1',
        ),
        migrations.RemoveField(
            model_name='team',
            name='evaluation_p2',
        ),
        migrations.RemoveField(
            model_name='team',
            name='evaluation_p3',
        ),
        migrations.RemoveField(
            model_name='team',
            name='evaluation_p4',
        ),
        migrations.RemoveField(
            model_name='team',
            name='evaluation_p5',
        ),
        migrations.RemoveField(
            model_name='team',
            name='evaluation_p6',
        ),
        migrations.RemoveField(
            model_name='team',
            name='evaluation_p7',
        ),
        migrations.AlterField(
            model_name='team',
            name='projects',
            field=models.ManyToManyField(blank=True, null=True, to='users.Project'),
        ),
        migrations.CreateModel(
            name='TeamEvaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('evaluation_p1', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('evaluation_p2', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('evaluation_p3', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('evaluation_p4', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('evaluation_p5', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('evaluation_p6', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('evaluation_p7', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='evaluation',
            field=models.ManyToManyField(related_name='evaluated_teams', through='users.TeamEvaluation', to=settings.AUTH_USER_MODEL),
        ),
    ]
