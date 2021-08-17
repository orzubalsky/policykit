# Generated by Django 3.2.2 on 2021-08-16 19:18

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import policyengine.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_bundled', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('readable_name', models.CharField(blank=True, max_length=300)),
                ('metagov_slug', models.SlugField(blank=True, max_length=36, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CommunityPlatform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community_name', models.CharField(max_length=1000, verbose_name='team_name')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='CommunityUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('readable_name', models.CharField(max_length=300, null=True, verbose_name='readable_name')),
                ('access_token', models.CharField(max_length=300, null=True, verbose_name='access_token')),
                ('is_community_admin', models.BooleanField(default=False)),
                ('avatar', models.CharField(max_length=500, null=True, verbose_name='avatar')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policyengine.communityplatform')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_policyengine.communityuser_set+', to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user', models.Model),
            managers=[
                ('objects', policyengine.models.PolymorphicUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='DataStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_store', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('platform', 'platform'), ('constitution', 'constitution')], max_length=30)),
                ('filter', models.TextField(blank=True, default='')),
                ('initialize', models.TextField(blank=True, default='')),
                ('check', models.TextField(blank=True, default='')),
                ('notify', models.TextField(blank=True, default='')),
                ('success', models.TextField(blank=True, default='')),
                ('fail', models.TextField(blank=True, default='')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('bundled_policies', models.ManyToManyField(blank=True, related_name='member_of_bundle', to='policyengine.Policy')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policyengine.communityplatform', verbose_name='community')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ConstitutionAction',
            fields=[
                ('baseaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.baseaction')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('policyengine.baseaction', models.Model),
        ),
        migrations.CreateModel(
            name='PlatformAction',
            fields=[
                ('baseaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.baseaction')),
                ('community_revert', models.BooleanField(default=False)),
                ('community_origin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('policyengine.baseaction', models.Model),
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proposal_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('proposed', 'proposed'), ('failed', 'failed'), ('passed', 'passed')], max_length=10)),
                ('community_post', models.CharField(blank=True, max_length=300)),
                ('governance_process_url', models.URLField(blank=True, max_length=100)),
                ('governance_process_json', models.JSONField(blank=True, null=True)),
                ('action', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='policyengine.baseaction')),
                ('data', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='policyengine.datastore')),
                ('policy', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='policyengine.policy')),
            ],
        ),
        migrations.CreateModel(
            name='NumberVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_time', models.DateTimeField(auto_now_add=True)),
                ('number_value', models.IntegerField(null=True)),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policyengine.proposal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policyengine.communityuser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LogAPICall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proposal_time', models.DateTimeField(auto_now_add=True)),
                ('call_type', models.CharField(max_length=300, verbose_name='call_type')),
                ('extra_info', models.TextField()),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policyengine.communityplatform')),
            ],
        ),
        migrations.CreateModel(
            name='CommunityRole',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.group')),
                ('role_name', models.TextField(max_length=300, null=True, verbose_name='readable_name')),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('community', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='policyengine.communityplatform')),
            ],
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.AddField(
            model_name='communityplatform',
            name='base_role',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='base_community', to='policyengine.communityrole'),
        ),
        migrations.AddField(
            model_name='communityplatform',
            name='community',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policyengine.community'),
        ),
        migrations.AddField(
            model_name='communityplatform',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_policyengine.communityplatform_set+', to='contenttypes.contenttype'),
        ),
        migrations.CreateModel(
            name='CommunityDoc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, default='', null=True)),
                ('text', models.TextField(blank=True, default='', null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('community', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='policyengine.communityplatform')),
            ],
        ),
        migrations.CreateModel(
            name='BooleanVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_time', models.DateTimeField(auto_now_add=True)),
                ('boolean_value', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True, null=True)),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policyengine.proposal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policyengine.communityuser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='baseaction',
            name='community',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policyengine.communityplatform', verbose_name='community'),
        ),
        migrations.AddField(
            model_name='baseaction',
            name='initiator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='policyengine.communityuser'),
        ),
        migrations.AddField(
            model_name='baseaction',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_policyengine.baseaction_set+', to='contenttypes.contenttype'),
        ),
        migrations.CreateModel(
            name='EditorModel',
            fields=[
                ('constitutionaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.constitutionaction')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('filter', models.TextField(blank=True, default='return True\n\n', verbose_name='Filter')),
                ('initialize', models.TextField(blank=True, default='pass\n\n', verbose_name='Initialize')),
                ('check', models.TextField(blank=True, default='return PASSED\n\n', verbose_name='Check')),
                ('notify', models.TextField(blank=True, default='pass\n\n', verbose_name='Notify')),
                ('success', models.TextField(blank=True, default='action.execute()\n\n', verbose_name='Pass')),
                ('fail', models.TextField(blank=True, default='pass\n\n', verbose_name='Fail')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('policyengine.constitutionaction',),
        ),
        migrations.CreateModel(
            name='PolicykitAddCommunityDoc',
            fields=[
                ('constitutionaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.constitutionaction')),
                ('name', models.TextField()),
                ('text', models.TextField()),
            ],
            options={
                'permissions': (('can_execute_policykitaddcommunitydoc', 'Can execute policykit add community doc'),),
            },
            bases=('policyengine.constitutionaction',),
        ),
        migrations.CreateModel(
            name='PlatformActionBundle',
            fields=[
                ('baseaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.baseaction')),
                ('bundle_type', models.CharField(choices=[('election', 'election'), ('bundle', 'bundle')], max_length=10)),
                ('bundled_actions', models.ManyToManyField(to='policyengine.PlatformAction')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('policyengine.baseaction',),
        ),
        migrations.CreateModel(
            name='ConstitutionActionBundle',
            fields=[
                ('baseaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.baseaction')),
                ('bundle_type', models.CharField(choices=[('election', 'election'), ('bundle', 'bundle')], max_length=10)),
                ('bundled_actions', models.ManyToManyField(to='policyengine.ConstitutionAction')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('policyengine.baseaction',),
        ),
        migrations.CreateModel(
            name='PolicykitAddConstitutionPolicy',
            fields=[
                ('editormodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.editormodel')),
            ],
            options={
                'permissions': (('can_execute_policykitaddconstitutionpolicy', 'Can execute policykit add constitution policy'),),
            },
            bases=('policyengine.editormodel',),
        ),
        migrations.CreateModel(
            name='PolicykitAddPlatformPolicy',
            fields=[
                ('editormodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.editormodel')),
            ],
            options={
                'permissions': (('can_execute_addpolicykitplatformpolicy', 'Can execute policykit add platform policy'),),
            },
            bases=('policyengine.editormodel',),
        ),
        migrations.CreateModel(
            name='PolicykitRemoveUserRole',
            fields=[
                ('constitutionaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.constitutionaction')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policyengine.communityrole')),
                ('users', models.ManyToManyField(to='policyengine.CommunityUser')),
            ],
            options={
                'permissions': (('can_execute_policykitremoveuserrole', 'Can execute policykit remove user role'),),
            },
            bases=('policyengine.constitutionaction',),
        ),
        migrations.CreateModel(
            name='PolicykitRemovePlatformPolicy',
            fields=[
                ('constitutionaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.constitutionaction')),
                ('platform_policy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='policyengine.policy')),
            ],
            options={
                'permissions': (('can_execute_policykitremoveplatformpolicy', 'Can execute policykit remove platform policy'),),
            },
            bases=('policyengine.constitutionaction',),
        ),
        migrations.CreateModel(
            name='PolicykitRemoveConstitutionPolicy',
            fields=[
                ('constitutionaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.constitutionaction')),
                ('constitution_policy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='policyengine.policy')),
            ],
            options={
                'permissions': (('can_execute_policykitremoveconstitutionpolicy', 'Can execute policykit remove constitution policy'),),
            },
            bases=('policyengine.constitutionaction',),
        ),
        migrations.CreateModel(
            name='PolicykitRecoverPlatformPolicy',
            fields=[
                ('constitutionaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.constitutionaction')),
                ('platform_policy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='policyengine.policy')),
            ],
            options={
                'permissions': (('can_execute_policykitrecoverplatformpolicy', 'Can execute policykit recover platform policy'),),
            },
            bases=('policyengine.constitutionaction',),
        ),
        migrations.CreateModel(
            name='PolicykitRecoverConstitutionPolicy',
            fields=[
                ('constitutionaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.constitutionaction')),
                ('constitution_policy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='policyengine.policy')),
            ],
            options={
                'permissions': (('can_execute_policykitrecoverconstitutionpolicy', 'Can execute policykit recover constitution policy'),),
            },
            bases=('policyengine.constitutionaction',),
        ),
        migrations.CreateModel(
            name='PolicykitRecoverCommunityDoc',
            fields=[
                ('constitutionaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.constitutionaction')),
                ('doc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='policyengine.communitydoc')),
            ],
            options={
                'permissions': (('can_execute_policykitrecovercommunitydoc', 'Can execute policykit recover community doc'),),
            },
            bases=('policyengine.constitutionaction',),
        ),
        migrations.CreateModel(
            name='PolicykitEditRole',
            fields=[
                ('constitutionaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.constitutionaction')),
                ('name', models.CharField(max_length=300, verbose_name='name')),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('permissions', models.ManyToManyField(to='auth.Permission')),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='policyengine.communityrole')),
            ],
            options={
                'permissions': (('can_execute_policykiteditrole', 'Can execute policykit edit role'),),
            },
            bases=('policyengine.constitutionaction',),
        ),
        migrations.CreateModel(
            name='PolicykitDeleteRole',
            fields=[
                ('constitutionaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.constitutionaction')),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='policyengine.communityrole')),
            ],
            options={
                'permissions': (('can_execute_policykitdeleterole', 'Can execute policykit delete role'),),
            },
            bases=('policyengine.constitutionaction',),
        ),
        migrations.CreateModel(
            name='PolicykitDeleteCommunityDoc',
            fields=[
                ('constitutionaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.constitutionaction')),
                ('doc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='policyengine.communitydoc')),
            ],
            options={
                'permissions': (('can_execute_policykitdeletecommunitydoc', 'Can execute policykit delete community doc'),),
            },
            bases=('policyengine.constitutionaction',),
        ),
        migrations.CreateModel(
            name='PolicykitChangeCommunityDoc',
            fields=[
                ('constitutionaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.constitutionaction')),
                ('name', models.TextField()),
                ('text', models.TextField()),
                ('doc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='policyengine.communitydoc')),
            ],
            options={
                'permissions': (('can_execute_policykitchangecommunitydoc', 'Can execute policykit change community doc'),),
            },
            bases=('policyengine.constitutionaction',),
        ),
        migrations.CreateModel(
            name='PolicykitAddUserRole',
            fields=[
                ('constitutionaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.constitutionaction')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policyengine.communityrole')),
                ('users', models.ManyToManyField(to='policyengine.CommunityUser')),
            ],
            options={
                'permissions': (('can_execute_policykitadduserrole', 'Can execute policykit add user role'),),
            },
            bases=('policyengine.constitutionaction',),
        ),
        migrations.CreateModel(
            name='PolicykitAddRole',
            fields=[
                ('constitutionaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.constitutionaction')),
                ('name', models.CharField(max_length=300, verbose_name='name')),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('permissions', models.ManyToManyField(to='auth.Permission')),
            ],
            options={
                'permissions': (('can_execute_policykitaddrole', 'Can execute policykit add role'),),
            },
            bases=('policyengine.constitutionaction',),
        ),
        migrations.CreateModel(
            name='PolicykitChangePlatformPolicy',
            fields=[
                ('editormodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.editormodel')),
                ('platform_policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policyengine.policy')),
            ],
            options={
                'permissions': (('can_execute_policykitchangeplatformpolicy', 'Can execute policykit change platform policy'),),
            },
            bases=('policyengine.editormodel',),
        ),
        migrations.CreateModel(
            name='PolicykitChangeConstitutionPolicy',
            fields=[
                ('editormodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='policyengine.editormodel')),
                ('constitution_policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policyengine.policy')),
            ],
            options={
                'permissions': (('can_execute_policykitchangeconstitutionpolicy', 'Can execute policykit change constitution policy'),),
            },
            bases=('policyengine.editormodel',),
        ),
    ]
