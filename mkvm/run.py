#!/usr/bin/env python3

import click

from mkvm.file import File
from mkvm.mkv_file import MkvFile
from mkvm.pipeline import Pipeline

from mkvm.stages import AddSubtitles, Convert


pipeline = Pipeline()


@click.group()
def action():
    pass


@action.command()
@click.argument('file', nargs=1)
@click.option('--raw', '-r', default=False, is_flag=True)
def inspect(file, raw):
    mkv_file = MkvFile(file)
    if raw:
        click.echo(mkv_file.as_raw())
    else:
        click.echo(mkv_file.as_table())


@action.group(chain=True)
@click.argument('file', nargs=1)
def process(file):
    pipeline.input_file = File(file)


@process.command(name='encode_audio')
@click.option('--default/--no-default', 'default', default=False)
def encode_audio(default):
    pipeline.convert_stage.set_encode_audio(default)


@process.command(name='strip_subs')
def strip_subs():
    pipeline.convert_stage.set_strip_subs()


@process.command(name='default_audio')
@click.argument('audio_track_id', nargs=1, type=int)
def default_audio(audio_track_id):
    pipeline.convert_stage.set_default_audio(audio_track_id)


@process.command(name='default_subtitles')
@click.argument('subtitles_track_id', nargs=1, type=int)
def default_subtitles(subtitles_track_id):
    pipeline.convert_stage.set_default_subtitles(subtitles_track_id)


@process.command(name='add_subtitles')
@click.argument('subtitles_file', nargs=1)
@click.option('--shift', 'shift', default=None)
def add_subtitles(subtitles_file, shift):
    pipeline.stages.append(AddSubtitles(subtitles_file, shift=shift))


@process.resultcallback()
@click.pass_context
def process_end(*args, **kwargs):
    pipeline.run()


if __name__ == '__main__':
    action()
