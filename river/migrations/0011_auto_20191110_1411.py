# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-11-10 20:11
from __future__ import unicode_literals

from uuid import uuid4

import django.db.models.deletion
from django.db import migrations, models


def migrate_transition_hook(apps, schema_editor):
    OnTransitHook = apps.get_model('river', 'OnTransitHook')
    Transition = apps.get_model('river', 'Transition')
    TransitionMeta = apps.get_model('river', 'TransitionMeta')

    for on_transition_hook in OnTransitHook.objects.all():
        if on_transition_hook.object_id:
            transition = Transition.objects.filter(
                workflow=on_transition_hook.workflow,
                source_state=on_transition_hook.source_state,
                destination_state=on_transition_hook.destination_state,
                object_id=on_transition_hook.object_id,
            )
            if on_transition_hook.iteration:
                transition = transition.include(iteration=on_transition_hook.iteration)

            transition = transition.first()
            if transition:
                on_transition_hook.transition_meta = transition.meta
                on_transition_hook.transition = transition
                on_transition_hook.save()


        else:
            transition_meta = TransitionMeta.objects.filter(
                workflow=on_transition_hook.workflow,
                source_state=on_transition_hook.source_state,
                destination_state=on_transition_hook.destination_state,

            ).first()
            if transition_meta:
                on_transition_hook.transition_meta = transition_meta
                on_transition_hook.save()


def reverse_transition_hook_migration(apps, schema_editor):
    OnTransitHook = apps.get_model('river', 'OnTransitHook')

    for on_transition_hook in OnTransitHook.objects.all():
        on_transition_hook.source_state = on_transition_hook.transition_meta.source_state
        on_transition_hook.destination_state = on_transition_hook.transition_meta.destination_state

        if on_transition_hook.transition:
            on_transition_hook.iteration = on_transition_hook.iteration


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('river', '0010_auto_20191110_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='ontransithook',
            name='iteration',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Priority'),
        ),
        migrations.AddField(
            model_name='ontransithook',
            name='transition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='on_transit_hooks', to='river.Transition', verbose_name='Transition'),
        ),
        migrations.AddField(
            model_name='ontransithook',
            name='transition_meta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='on_transit_hooks', to='river.TransitionMeta', verbose_name='Transition Meta'),
        ),
        migrations.AlterField(
            model_name='ontransithook',
            name='destination_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='on_transition_hook_as_destination', to='river.State', verbose_name='Next State'),
        ),
        migrations.AlterField(
            model_name='ontransithook',
            name='source_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='on_transition_hook_as_source', to='river.State', verbose_name='Source State'),
        ),
        migrations.AlterUniqueTogether(
            name='ontransithook',
            unique_together=set([('callback_function', 'workflow', 'transition_meta', 'content_type', 'object_id', 'transition')]),
        ),

        migrations.RunPython(migrate_transition_hook, reverse_code=reverse_transition_hook_migration),

        migrations.AlterField(
            model_name='ontransithook',
            name='destination_state',
            field=models.CharField(verbose_name='destination_state', max_length=200, default=uuid4),
            preserve_default=True,
        ),

        migrations.RemoveField(
            model_name='ontransithook',
            name='destination_state',
        ),

        migrations.AlterField(
            model_name='ontransithook',
            name='iteration',
            field=models.CharField(verbose_name='iteration', max_length=200, default=uuid4),
            preserve_default=True,
        ),

        migrations.RemoveField(
            model_name='ontransithook',
            name='iteration',
        ),

        migrations.AlterField(
            model_name='ontransithook',
            name='source_state',
            field=models.CharField(verbose_name='source_state', max_length=200, default=uuid4),
            preserve_default=True,
        ),

        migrations.RemoveField(
            model_name='ontransithook',
            name='source_state',
        ),

        migrations.AlterField(
            model_name='ontransithook',
            name='transition_meta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='on_transit_hooks', to='river.TransitionMeta', verbose_name='Transition Meta'),
        ),

        migrations.AlterField(
            model_name='onapprovedhook',
            name='transition_approval',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='on_approved_hooks', to='river.TransitionApproval',
                                    verbose_name='Transition Approval'),
        ),
        migrations.AlterField(
            model_name='onapprovedhook',
            name='transition_approval_meta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='on_approved_hooks', to='river.TransitionApprovalMeta', verbose_name='Transition Approval Meta'),
        ),
        migrations.AlterField(
            model_name='ontransithook',
            name='transition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='on_transit_hooks', to='river.Transition', verbose_name='Transition'),
        ),
        migrations.AlterField(
            model_name='ontransithook',
            name='transition_meta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='on_transit_hooks', to='river.TransitionMeta', verbose_name='Transition Meta'),
        ),
    ]