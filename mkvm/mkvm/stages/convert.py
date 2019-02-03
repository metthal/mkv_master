from mkvm.pipeline import PipelineStage
from mkvm.process import Process


class Convert(PipelineStage):
    DEFAULT_ENCODE_AUDIO = False
    DEFAULT_STRIP_SUBS = False
    DEFAULT_DEFAULT_AUDIO = False
    DEFAULT_DEFAULT_SUBTITLES = False

    def __init__(self, encode_audio=DEFAULT_ENCODE_AUDIO, strip_subs=DEFAULT_STRIP_SUBS, default_audio=DEFAULT_DEFAULT_AUDIO, default_subtitles=DEFAULT_DEFAULT_SUBTITLES):
        super(Convert, self).__init__()

        self.encode_audio = encode_audio
        self.strip_subs = strip_subs
        self.default_audio = default_audio
        self.default_subtitles = default_subtitles

        self.encode_audio_as_default = False
        self.default_audio_track_id = None
        self.default_subtitles_track_id = None

    def passthrough(self):
        return self.encode_audio == Convert.DEFAULT_ENCODE_AUDIO \
            and self.strip_subs == Convert.DEFAULT_STRIP_SUBS \
            and self.default_audio == Convert.DEFAULT_DEFAULT_AUDIO \
            and self.default_subtitles == Convert.DEFAULT_DEFAULT_SUBTITLES

    def set_encode_audio(self, as_default):
        self.encode_audio = True
        self.encode_audio_as_default = as_default

    def set_strip_subs(self):
        self.strip_subs = True

    def set_default_audio(self, audio_track_id):
        self.default_audio = True
        self.default_audio_track_id = audio_track_id

    def set_default_subtitles(self, subtitles_track_id):
        self.default_subtitles = True
        self.default_subtitles_track_id = subtitles_track_id

    def run(self, input_mkv_file, output_filepath):
        args = [
            '-y',
            '-i', input_mkv_file.path,
            '-map', '0', '-c', 'copy',
        ]

        if self.strip_subs:
            args.append('-sn')

        if self.default_audio:
            for i in range(input_mkv_file.number_of_audio_streams):
                args.extend(['-disposition:a:{}'.format(i), '0' if i != self.default_audio_track_id else 'default'])

        if self.default_subtitles:
            for i in range(input_mkv_file.number_of_subtitle_streams):
                args.extend(['-disposition:s:{}'.format(i), '0' if i != self.default_subtitles_track_id else 'default'])

        if self.encode_audio:
            args.extend(['-map', '0:a:{}'.format(input_mkv_file.best_audio_stream), '-c:a:{}'.format(input_mkv_file.number_of_audio_streams), 'libfdk_aac', '-b:a', '896k'])
            if self.encode_audio_as_default:
                args.extend(['-disposition:a:{}'.format(input_mkv_file.number_of_audio_streams), 'default'])

        args.append(output_filepath)

        ffmpeg = Process('ffmpeg')
        ffmpeg.run(args)
