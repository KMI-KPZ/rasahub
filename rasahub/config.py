import argparse
import inspect
import yaml

def create_argparser():
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

    return config

def save_config(config, filename):
    with open(filename, 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)

if __name__ == '__main__':
    parser = create_argparser()
    arguments = parser.parse_args()

    filename = arguments.output
    plugins = arguments.plugins

    config = create_config(plugins)
    save_config(config, filename)
