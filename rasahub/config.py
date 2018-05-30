import argparse
import inspect
import yaml

def create_argparser():
    """Creates and returns the argument parser for config creation.

    Returns:
        ArgumentParser

    """

    parser = argparse.ArgumentParser(description='Creates the Rasahub configuration file.')
    parser.add_argument(
            '-o', '--output',
            type=str,
            default='config.yml',
            help="Config file name to create")
    parser.add_argument(
            '-p', '--plugins',
            nargs='+',
            required=True,
            help="Plugin name")

    return parser

def create_config(plugins):
    """Creates and returns the configuration given plugin names

    Args:
        plugins: List of plugins to include in config

    Returns:
        configuration as dict

    """
    config = {}
    for plugin in plugins:
        pluginname = plugin
        while pluginname in config:
            pluginname = pluginname + '2'
        config[pluginname] = {}
        config[pluginname]['package'] = plugin # TODO no rasahub_ prefix
        config[pluginname]['init'] = {}
        # fill initialization
        lib = __import__(plugin)
        classes = inspect.getmembers(lib, inspect.isclass)
        pluginclass = None
        for plugin_class in classes:
            if plugin_class[1].__bases__[0].__name__ == 'RasahubPlugin':
                pluginclass = plugin_class[1]
        varnames = pluginclass.__init__.__code__.co_varnames[:pluginclass.__init__.__code__.co_argcount]
        for index in range(len(varnames)):
            if index > 0 and varnames[index] != 'self' and varnames[index] != 'kwargs':
                config[pluginname]['init'][varnames[index]] = pluginclass.__init__.__defaults__[index-1]

        config[pluginname]['out'] = ""
        for other_plugin in config:
            if pluginname != other_plugin:
                config[pluginname]['out'] = other_plugin

        config[pluginname]['type'] = "datastore"
        # check if there are send and receive methods - then its an interface or interpreter
        interface_methods = [m for m in members if m[0] == 'send' or m[0] == 'receive']
        if len(interface_methods) == 2:
            config[pluginname]['type'] = "interface"

    return config

def save_config(config, filename):
    """Saves config to given filename in yaml format

    Args:
        config: dict containing configuration arguments for each plugin
        filename: Filename to write yaml to

    """

    with open(filename, 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)

if __name__ == '__main__':
    parser = create_argparser()
    arguments = parser.parse_args()

    filename = arguments.output
    plugins = arguments.plugins

    config = create_config(plugins)
    save_config(config, filename)
