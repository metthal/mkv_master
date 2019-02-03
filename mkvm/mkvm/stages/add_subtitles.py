from mkvm.file import File
from mkvm.pipeline import PipelineStage
from mkvm.process import Process


class AddSubtitles(PipelineStage):
    def __init__(self, subtitles_filepath, shift=None):
        self.subtitles_filepath = subtitles_filepath
        self.shift = shift

    def run(self, input_mkv_file, output_filepath):
        try:
            subtitles_file = File(self.subtitles_filepath)
            if self.shift is not None:
                subtitles_file = File.temp('srt')
                self._shift_impl(subtitles_file)

            mkvmerge = Process('mkvmerge')
            mkvmerge.run([
                '-o', output_filepath,
                input_mkv_file.path,
                '--language', '0:eng',
                subtitles_file.path
            ])
        finally:
            subtitles_file.close()

    def _shift_impl(self, shifted_subs_file):
        srt = Process('srt')
        srt_rc, srt_output = srt.run([
            'shift', self.shift,
            self.subtitles_filepath
        ], return_output=True)

        if srt_rc != 0:
            raise ValueError('Failed to shift subtitles:\n\n{}'.format(srt_output))

        with open(shifted_subs_file.path, 'wb') as f:
            f.write(srt_output)
