import os
import shutil

from mkvm.file import File
from mkvm.mkv_file import MkvFile


class Pipeline:
    def __init__(self):
        from mkvm.stages import Convert
        self.input_file = File.none()
        self.convert_stage = Convert()
        self.stages = []

    @property
    def output_filepath(self):
        return os.path.join(os.path.dirname(self.input_file.path), 'mkvm_{}'.format(os.path.basename(self.input_file.path)))

    def run(self):
        assert self.input_file.path is not None

        try:
            input_file = self.input_file
            output_file = File.none()

            for stage in self.all_stages[:-1]:
                output_file = File.temp('mkv')
                stage.run(MkvFile(input_file.path), output_file.path)
                input_file.close()
                input_file = output_file

            try:
                last_stage = self.all_stages[-1]
                last_stage.run(MkvFile(input_file.path), self.output_filepath)
                input_file.close()
            except IndexError:
                pass
        finally:
            input_file.close()
            output_file.close()

    @property
    def all_stages(self):
        return list(filter(lambda s: not s.passthrough(), [self.convert_stage] + self.stages))


class PipelineStage:
    def run(self, input_filepath, output_filepath):
        raise NotImplementedError

    def passthrough(self):
        return False
