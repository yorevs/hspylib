#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hspylib.addons.widman.widget import Widget
from hspylib.core.enums.exit_code import ExitCode
from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.icons.font_awesome.widget_icons import WidgetIcons
from hspylib.modules.cli.menu.menu_utils import MenuUtils


class Widget_WIDGET_NAME_(Widget):

    WIDGET_ICON  = WidgetIcons.WIDGET
    WIDGET_NAME = "_WIDGET_NAME_"
    TOOLTIP = "TODO usage."
    USAGE = "Usage: _WIDGET_NAME_"
    VERSION = (0, 1, 0)

    def __init__(self):
        super().__init__(
            self.WIDGET_ICON,
            self.WIDGET_NAME,
            self.TOOLTIP,
            self.USAGE,
            self.VERSION)


    def execute(self, *args) -> ExitCode:
        # Include the widget's main code
        sysout('')
        sysout('My widget is running')
        sysout('')

        MenuUtils.wait_enter()

        return ExitCode.SUCCESS

    def cleanup(self):
        # If your widget requires any cleanup procedures
        pass
