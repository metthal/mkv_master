from mkvm.pipeline import PipelineStage
from mkvm.process import Process


class Convert(PipelineStage):
    DEFAULT_ENCODE_AUDIO = False
    DEFAULT_STRIP_SUBS = False

    def __init__(self, encode_audio=DEFAULT_ENCODE_AUDIO, strip_subs=DEFAULT_STRIP_SUBS):
        super(Convert, self).__init__()

        self.encode_audio = encode_audio
        self.strip_subs = strip_subs

        self.encode_audio_as_default = False

    def passthrough(self):
        return self.encode_audio == Convert.DEFAULT_ENCODE_AUDIO \
            and self.strip_subs == Convert.DEFAULT_STRIP_SUBS

    def set_encode_audio(self, as_default):
        self.encode_audio = True
        self.encode_audio_as_default = as_default

    def set_strip_subs(self):
        self.strip_subs = True

    def run(self, input_mkv_file, output_filepath):
        args = [
            '-y',
            '-i', input_mkv_file.path,
            '-map', '0', '-c', 'copy',
        ]

        if self.strip_subs:
            args.append('-sn')

        if self.encode_audio:
            args.extend(['-map', '0:a:{}'.format(input_mkv_file.best_audio_stream), '-c:a:{}'.format(input_mkv_file.number_of_audio_streams), 'libfdk_aac', '-b:a', '896k'])
            if self.encode_audio_as_default:
                args.extend(['-disposition:a:{}'.format(input_mkv_file.number_of_audio_streams), 'default'])

        args.append(output_filepath)

        ffmpeg = Process('ffmpeg')
        ffmpeg.run(args)
