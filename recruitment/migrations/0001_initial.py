# Generated by Django 4.2.7 on 2024-02-17 05:11

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import recruitment.models
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('horilla_audit', '0001_initial'),
        ('base', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Name')),
                ('profile', models.ImageField(null=True, upload_to='recruitment/profile')),
                ('portfolio', models.URLField(blank=True)),
                ('schedule_date', models.DateTimeField(blank=True, null=True, verbose_name='Schedule date')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('mobile', models.CharField(blank=True, max_length=15, validators=[recruitment.models.validate_mobile], verbose_name='Phone')),
                ('resume', models.FileField(upload_to='recruitment/resume', validators=[recruitment.models.validate_pdf])),
                ('address', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('country', models.CharField(blank=True, max_length=30, null=True, verbose_name='Country')),
                ('dob', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('state', models.CharField(blank=True, max_length=30, null=True, verbose_name='State')),
                ('city', models.CharField(blank=True, max_length=30, null=True, verbose_name='City')),
                ('zip', models.CharField(blank=True, max_length=30, null=True, verbose_name='Zip Code')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=15, null=True, verbose_name='Gender')),
                ('source', models.CharField(blank=True, choices=[('application', 'Application Form'), ('software', 'Inside software'), ('other', 'Other')], max_length=20, null=True, verbose_name='Source')),
                ('start_onboard', models.BooleanField(default=False, verbose_name='Start Onboard')),
                ('hired', models.BooleanField(default=False, verbose_name='Hired')),
                ('canceled', models.BooleanField(default=False, verbose_name='Canceled')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('joining_date', models.DateField(blank=True, null=True, verbose_name='Joining Date')),
                ('sequence', models.IntegerField(default=0, null=True)),
                ('probation_end', models.DateField(editable=False, null=True)),
                ('offer_letter_status', models.CharField(choices=[('not_sent', 'Not Sent'), ('sent', 'Sent'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('joined', 'Joined')], default='not_sent', editable=False, max_length=10)),
                ('last_updated', models.DateField(auto_now=True, null=True)),
                ('job_position_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='base.jobposition', verbose_name='Job Position')),
            ],
            options={
                'ordering': ['sequence'],
                'permissions': (('view_history', 'View Candidate History'), ('archive_candidate', 'Archive Candidate')),
            },
        ),
        migrations.CreateModel(
            name='Recruitment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=30, null=True)),
                ('description', models.TextField(null=True)),
                ('is_event_based', models.BooleanField(default=False, help_text='To start bulk recruitment form multiple job positions')),
                ('closed', models.BooleanField(default=False, help_text='To close the recruitment, If closed then not visible on pipeline view.')),
                ('is_published', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True, help_text='To archive and un-archive a recruitment, if active is false then it             will not appear on recruitment list view.')),
                ('vacancy', models.IntegerField(default=0, null=True)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('company_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='base.company', verbose_name='Company')),
                ('job_position_id', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='recruitment', to='base.jobposition', verbose_name='Job Position')),
                ('open_positions', models.ManyToManyField(blank=True, related_name='open_positions', to='base.jobposition')),
                ('recruitment_managers', models.ManyToManyField(to='employee.employee')),
            ],
            options={
                'permissions': (('archive_recruitment', 'Archive Recruitment'),),
                'unique_together': {('job_position_id', 'start_date'), ('job_position_id', 'start_date', 'company_id')},
            },
        ),
        migrations.CreateModel(
            name='SkillZone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Skill Zone')),
                ('description', models.TextField(verbose_name='Description')),
                ('created_on', models.DateField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.CharField(max_length=50)),
                ('stage_type', models.CharField(choices=[('initial', 'Initial'), ('test', 'Test'), ('interview', 'Interview'), ('hired', 'Hired')], default='interview', max_length=20)),
                ('sequence', models.IntegerField(default=0, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('recruitment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stage_set', to='recruitment.recruitment', verbose_name='Recruitment')),
                ('stage_managers', models.ManyToManyField(to='employee.employee')),
            ],
            options={
                'ordering': ['sequence'],
                'permissions': (('archive_Stage', 'Archive Stage'),),
                'unique_together': {('recruitment_id', 'stage')},
            },
        ),
        migrations.CreateModel(
            name='StageFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('files', models.FileField(blank=True, null=True, upload_to='recruitment/stageFiles')),
            ],
        ),
        migrations.CreateModel(
            name='StageNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, null=True, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('candidate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruitment.candidate')),
                ('stage_files', models.ManyToManyField(blank=True, to='recruitment.stagefiles')),
                ('stage_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruitment.stage')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee')),
            ],
        ),
        migrations.CreateModel(
            name='RejectReason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
                ('company_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.company')),
            ],
        ),
        migrations.CreateModel(
            name='RejectedCandidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('candidate_id', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='rejected_candidate', to='recruitment.candidate', verbose_name='Candidate')),
                ('reject_reason_id', models.ManyToManyField(blank=True, to='recruitment.rejectreason', verbose_name='Reject reason')),
            ],
        ),
        migrations.CreateModel(
            name='RecruitmentSurveyAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_json', models.JSONField()),
                ('attachment', models.FileField(blank=True, null=True, upload_to='recruitment_attachment')),
                ('candidate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruitment.candidate')),
                ('job_position_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='base.jobposition', verbose_name='Job Position')),
                ('recruitment_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='recruitment.recruitment', verbose_name='Recruitment')),
            ],
        ),
        migrations.CreateModel(
            name='RecruitmentSurvey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('sequence', models.IntegerField(default=0, null=True)),
                ('type', models.CharField(choices=[('checkbox', 'Yes/No'), ('options', 'Choices'), ('multiple', 'Multiple Choice'), ('text', 'Text'), ('number', 'Number'), ('percentage', 'Percentage'), ('date', 'Date'), ('textarea', 'Textarea'), ('file', 'File Upload'), ('rating', 'Rating')], max_length=15)),
                ('options', models.TextField(default='', help_text="Separate choices by ',  '", null=True)),
                ('is_mandatory', models.BooleanField(default=False)),
                ('job_position_ids', models.ManyToManyField(to='base.jobposition', verbose_name='Job Positions')),
                ('recruitment_ids', models.ManyToManyField(to='recruitment.recruitment', verbose_name='Recruitment')),
            ],
        ),
        migrations.CreateModel(
            name='RecruitmentMailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25, unique=True)),
                ('body', models.TextField()),
                ('company_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.company', verbose_name='Company')),
            ],
        ),
        migrations.CreateModel(
            name='RecruitmentGeneralSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate_self_tracking', models.BooleanField(default=False)),
                ('show_overall_rating', models.BooleanField(default=False)),
                ('company_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.company')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalRejectedCandidate',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('history_title', models.CharField(blank=True, max_length=20, null=True)),
                ('history_description', models.TextField(null=True)),
                ('history_highlight', models.BooleanField(default=False, null=True)),
                ('description', models.TextField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('candidate_id', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='recruitment.candidate', verbose_name='Candidate')),
                ('history_relation', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history_set', to='recruitment.rejectedcandidate')),
                ('history_tags', models.ManyToManyField(to='horilla_audit.audittag')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical rejected candidate',
                'verbose_name_plural': 'historical rejected candidates',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCandidate',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('history_title', models.CharField(blank=True, max_length=20, null=True)),
                ('history_description', models.TextField(null=True)),
                ('history_highlight', models.BooleanField(default=False, null=True)),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Name')),
                ('profile', models.TextField(max_length=100, null=True)),
                ('portfolio', models.URLField(blank=True)),
                ('schedule_date', models.DateTimeField(blank=True, null=True, verbose_name='Schedule date')),
                ('email', models.EmailField(db_index=True, max_length=254, verbose_name='Email')),
                ('mobile', models.CharField(blank=True, max_length=15, validators=[recruitment.models.validate_mobile], verbose_name='Phone')),
                ('resume', models.TextField(max_length=100, validators=[recruitment.models.validate_pdf])),
                ('address', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('country', models.CharField(blank=True, max_length=30, null=True, verbose_name='Country')),
                ('dob', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('state', models.CharField(blank=True, max_length=30, null=True, verbose_name='State')),
                ('city', models.CharField(blank=True, max_length=30, null=True, verbose_name='City')),
                ('zip', models.CharField(blank=True, max_length=30, null=True, verbose_name='Zip Code')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=15, null=True, verbose_name='Gender')),
                ('source', models.CharField(blank=True, choices=[('application', 'Application Form'), ('software', 'Inside software'), ('other', 'Other')], max_length=20, null=True, verbose_name='Source')),
                ('start_onboard', models.BooleanField(default=False, verbose_name='Start Onboard')),
                ('hired', models.BooleanField(default=False, verbose_name='Hired')),
                ('canceled', models.BooleanField(default=False, verbose_name='Canceled')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('joining_date', models.DateField(blank=True, null=True, verbose_name='Joining Date')),
                ('sequence', models.IntegerField(default=0, null=True)),
                ('probation_end', models.DateField(editable=False, null=True)),
                ('offer_letter_status', models.CharField(choices=[('not_sent', 'Not Sent'), ('sent', 'Sent'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('joined', 'Joined')], default='not_sent', editable=False, max_length=10)),
                ('last_updated', models.DateField(blank=True, editable=False, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_relation', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history_set', to='recruitment.candidate')),
                ('history_tags', models.ManyToManyField(to='horilla_audit.audittag')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('job_position_id', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='base.jobposition', verbose_name='Job Position')),
                ('recruitment_id', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='recruitment.recruitment', verbose_name='Recruitment')),
                ('referral', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='employee.employee', verbose_name='Referral')),
                ('stage_id', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='recruitment.stage', verbose_name='Stage')),
            ],
            options={
                'verbose_name': 'historical candidate',
                'verbose_name_plural': 'historical candidates',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddField(
            model_name='candidate',
            name='recruitment_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='candidate', to='recruitment.recruitment', verbose_name='Recruitment'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='referral',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='candidate_referral', to='employee.employee', verbose_name='Referral'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='stage_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='recruitment.stage', verbose_name='Stage'),
        ),
        migrations.CreateModel(
            name='SkillZoneCandidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=200, verbose_name='Reason')),
                ('added_on', models.DateField(default=django.utils.timezone.now, editable=False)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('candidate_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='skillzonecandidate_set', to='recruitment.candidate', verbose_name='Candidate')),
                ('skill_zone_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='skillzonecandidate_set', to='recruitment.skillzone', verbose_name='Skill Zone')),
            ],
            options={
                'unique_together': {('skill_zone_id', 'candidate_id')},
            },
        ),
        migrations.CreateModel(
            name='CandidateRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('candidate_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='candidate_rating', to='recruitment.candidate')),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='candidate_rating', to='employee.employee')),
            ],
            options={
                'unique_together': {('employee_id', 'candidate_id')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='candidate',
            unique_together={('email', 'recruitment_id')},
        ),
    ]
