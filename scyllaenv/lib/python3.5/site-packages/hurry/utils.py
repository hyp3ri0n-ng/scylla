import os
import json


class CommandList:
    def __init__(self, prefix):
        self._prefix = prefix
        self._string = "Usage:"

    def add_command(self, command):
        self._string += "\n    {prefix} {command}".format(
            command=command,
            prefix=self._prefix
        )

    def to_string(self):
        return self._string

    def add_config(self, config):
        for command in config:
            self.add_command(command)


class ExecChooser:
    def __init__(self, config):
        self._config = config

    def get_exec(self, parsed_arguments):
        enabled_arguments = {argument: value for argument, value
                             in parsed_arguments.items() if value}
        return self._get_exec(enabled_arguments)

    def _get_exec(self, enabled_arguments):
        config_key = self._get_config_key(enabled_arguments)
        exec_value = self._config[config_key]
        for argument, value in enabled_arguments.items():
            if not isinstance(value, bool):
                exec_value = exec_value.replace(argument, value)
        return exec_value

    def _get_config_key(self, enabled_arguments):
        for config_key in self._config.keys():
            if set(config_key.split()) == set(enabled_arguments.keys()):
                return config_key


class ConfigReader:
    FILENAME = "hurry.json"

    def __init__(self, path):
        self._config_path = os.path.join(path, self.FILENAME)

    def get_dict(self):
        config = open(self._config_path)
        config_dict = json.load(config)
        config.close()
        return config_dict


