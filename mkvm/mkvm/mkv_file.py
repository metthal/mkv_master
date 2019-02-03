import json

from tabulate import tabulate

from mkvm.process import Process


CODEC_WEIGHT = {
    'dts': 2,
    'truehd': 2,
    'aac': 1,
    'ac3': 1
}

LANGUAGE_WEIGHT = {
    'eng': 2
}


class MkvFile:
    def __init__(self, path):
        self.path = path
        self.tracks = []

        ffprobe = Process('ffprobe')
        ffprobe_rc, ffprobe_output = ffprobe.run([
            '-v', '0',
            '-print_format', 'json',
            '-show_streams',
            self.path
        ], return_output=True)

        assert ffprobe_rc == 0
        self._info = json.loads(ffprobe_output)

    def as_table(self):
        video_streams = [[
            s['stream_id'],
            s['video_stream_id'],
            s['codec'],
            '[x]' if s['default'] else '[ ]',
            '{}x{}'.format(s['resolution']['width'], s['resolution']['height']),
            s['bitrate'],
            s['duration']
        ] for s in self.video_streams]

        best_audio_stream_id = self.best_audio_stream
        audio_streams = [[
            s['stream_id'],
            s['audio_stream_id'],
            s['codec'],
            '[x]' if s['default'] else '[ ]',
            s['channels'],
            s['bitrate'],
            s['language'],
            '[x]' if s['audio_stream_id'] == best_audio_stream_id else '[ ]'
        ] for s in self.audio_streams]

        subtitle_streams = [[
            s['stream_id'],
            s['subtitle_stream_id'],
            s['codec'],
            '[x]' if s['default'] else '[ ]',
            s['language']
        ] for s in self.subtitle_streams]

        return '\n\n'.join([
            'Video streams:\n' + tabulate(video_streams, headers=['ID', 'Video ID', 'Codec', 'Default', 'Resolution', 'Bitrate', 'Duration']),
            'Audio streams:\n' + tabulate(audio_streams, headers=['ID', 'Audio ID', 'Codec', 'Default', 'Channels', 'Bitrate', 'Language', 'Best']),
            'Subtitle streams:\n' + tabulate(subtitle_streams, headers=['ID', 'Sub ID', 'Codec', 'Default', 'Language']),
        ])

    def as_raw(self):
        return json.dumps(self._info, indent=True)

    @property
    def number_of_streams(self):
        return len(self._streams)

    @property
    def number_of_audio_streams(self):
        return len(self._streams_of_type('audio'))

    @property
    def best_audio_stream(self):
        return sorted([
            (
                LANGUAGE_WEIGHT.get(s['language'], 0),
                CODEC_WEIGHT.get(s['codec'], 0),
                s['channels'],
                s.get('bitrate', 0),
                s['audio_stream_id']
            ) for s in self.audio_streams], reverse=True)[0][4]

    @property
    def video_streams(self):
        return [MkvFile.video_stream_json(i, s) for i, s in enumerate(self._streams_of_type('video'))]

    @property
    def audio_streams(self):
        return [MkvFile.audio_stream_json(i, s) for i, s in enumerate(self._streams_of_type('audio'))]

    @property
    def subtitle_streams(self):
        return [MkvFile.subtitle_stream_json(i, s) for i, s in enumerate(self._streams_of_type('subtitle'))]

    @property
    def _streams(self):
        return self._info.get('streams', [])

    def _streams_of_type(self, type):
        return [s for s in self._streams if s['codec_type'] == type]

    @staticmethod
    def video_stream_json(video_stream_id, stream):
        return {
            'stream_id': stream['index'],
            'video_stream_id': video_stream_id,
            'codec': stream['codec_name'],
            'resolution': {
                'width': stream['width'],
                'height': stream['height']
            },
            'default': True if stream['disposition']['default'] == 1 else False,
            'bitrate': MkvFile._parse_bitrate(stream),
            'duration': MkvFile._parse_tag_value(stream, 'DURATION')
        }

    @staticmethod
    def audio_stream_json(audio_stream_id, stream):
        return {
            'stream_id': stream['index'],
            'audio_stream_id': audio_stream_id,
            'codec': stream['codec_name'],
            'channels': stream['channels'],
            'default': True if stream['disposition']['default'] == 1 else False,
            'bitrate': MkvFile._parse_bitrate(stream),
            'language': MkvFile._parse_tag_value(stream, 'language')
        }

    @staticmethod
    def subtitle_stream_json(subtitle_stream_id, stream):
        return {
            'stream_id': stream['index'],
            'subtitle_stream_id': subtitle_stream_id,
            'codec': stream['codec_name'],
            'default': True if stream['disposition']['default'] == 1 else False,
            'language': MkvFile._parse_tag_value(stream, 'language')
        }

    @staticmethod
    def _parse_bitrate(stream):
        def _calc_bitrate(val, div):
            return round(int(val) / div)

        if 'bit_rate' in stream:
            return _calc_bitrate(stream['bit_rate'], 1000)
        elif 'tags' in stream:
            bitrate = MkvFile._parse_tag_value(stream, 'BPS')
            if bitrate is not None:
                return _calc_bitrate(bitrate, 1024)

    @staticmethod
    def _parse_tag_value(stream, tag_name):
        if 'tags' in stream:
            if tag_name in stream['tags']:
                return stream['tags'][tag_name]
            else:
                for tag_key, tag_value in stream['tags'].items():
                    if tag_key.startswith(f'{tag_name}-'):
                        return tag_value
