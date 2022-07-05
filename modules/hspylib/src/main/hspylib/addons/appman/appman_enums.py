from hspylib.core.enums.enumeration import Enumeration


class Addon(Enumeration):
    """TODO"""
    APPMAN = 'appman'
    WIDGETS = 'widgets'


class Extension(Enumeration):
    """TODO"""
    GRADLE = 'gradle'
    GIT = 'git'


class AppType(Enumeration):
    """TODO"""
    APP = 'app'
    QT_APP = 'qt-app'
    WIDGET = 'widget'
