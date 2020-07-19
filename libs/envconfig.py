from os import environ as sysenv

__all__ = ['envconfig']

def _envtranslate(x):
    if type(x) == str:
        if x.isnumeric():
            return int(x)
        elif x.count('.') == 1 and x.replace('.','').isnumeric():
            return float(x)
        elif x.lower() in ['true', 'false']:
            return x.lower() == 'true'
        return x
    elif type(x) == tuple and len(x) == 2:
        return (x[0],_envtranslate(x[1]))
    return x

class _envconfig():
    def __init__(self):
        self.reload()
        # 习惯兼容层
        self.get = self.readConfig
        self.gets = self.readConfigs
        self.getdict = self.readConfigdict

    def reload(self):
        self._setting = {}
        self._setting.update(map(_envtranslate,sysenv.items()))

    def readConfig(self, Name, Default = None):
        return self._setting.get(Name,Default)

    def readConfigs(self, *Names, Default = None):
        return ( self._setting.get(Name,Default) for Name in Names )

    def readConfigdict(self, *Names, Default = None):
        return { Name:self._setting.get(Name,Default) for Name in Names }

envconfig = _envconfig()