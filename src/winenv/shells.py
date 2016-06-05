import abc


class ShellSyntax(abc.ABC):

    @abc.abstractmethod
    def export_variable(self, variable, value):
        raise NotImplementedError

    @abc.abstractmethod
    def unset_variable(self, variable):
        raise NotImplementedError

    @property
    def command_separator(self):
        return ';'


class BashSyntax(ShellSyntax):

    def export_variable(self, variable, value):
        return 'export {}="{}"'.format(variable, value)

    def unset_variable(self, variable):
        return 'unset {}'.format(variable)


class FishSyntax(ShellSyntax):

    def export_variable(self, variable, value):
        return 'set -gx {} "{}"'.format(variable, value)

    def unset_variable(self, variable):
        return 'set -e {}'.format(variable)

SHELLS = {
    'bash': BashSyntax(),
    'fish': FishSyntax(),
}

DEFAULT_SHELL = 'bash'
