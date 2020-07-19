
class en_US():
    @staticmethod
    def ValueOnlySupport(name, support_type, type):
        return '%s only support "%s", but not "%s"' % (name,support_type,type)

    @staticmethod
    def ValueSupportList(name, support_type, type):
        return '%s support "[%s]", but not "%s"' % (name,', '.join(support_type),type)

    @staticmethod
    def CPUModelRequired():
        return '"model" is required when \'mode\' = "custom"'

    @staticmethod
    def WatchdogOnlySupport(value):
        return 'Watchdog only support i6300esb, ib700 and diag288. But not "%s"' % value

    @staticmethod
    def WatchdogActionSupport(value):
        return 'Action "%s" not supported. Watchdog.action only support reset, shutdown, poweroff, pause, none, dump and inject-nmi' % value

class zh_CN():
    @staticmethod
    def ValueOnlySupport(name, support_type, type):
        return '不支持的类型 "%s"。%s 仅支持 "%s"。' % (type,name,support_type)

    @staticmethod
    def ValueSupportList(name, support_type, type):
        return '不支持的类型 "%s"。%s 支持 "[%s]"。' % (type,name,', '.join(support_type))

    @staticmethod
    def CPUModelRequired():
        return '当 mode="custom"时，model是必须的'

    @staticmethod
    def WatchdogOnlySupport(value):
        return '"%s"不支持。Watchdog 只支持 i6300esb、ib700 和 diag288 设备' % value

    @staticmethod
    def WatchdogActionSupport(value):
        return '动作"%s"不支持。Watchdog 只支持 reset、shutdown、poweroff、pause、none、dump、inject-nmi 动作' % value

Langlist = {
    'en_US': en_US,
    'zh_CN': zh_CN
}

def getLanguarge(lang = 'en_US'):
    return Langlist.get(lang, en_US)

