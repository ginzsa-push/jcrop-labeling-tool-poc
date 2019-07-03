import os
import json

plugins_path = './cropLabel/plugins'

plugins = []
plugins_map = {}

def getPlugins():
    # reset plugin list
    plugins = []
    #get directories only
    dirs = [d for d in os.listdir(plugins_path)
            if os.path.isdir(os.path.join(plugins_path, d))
            if not d.startswith('_')]

    for dir in dirs:
        js = open('{}/{}/properties.json'.format(plugins_path, dir)).read()
        plugin = json.loads(js)
        plugins.append(plugin)
        plugins_map[dir] = plugin

    return plugins
