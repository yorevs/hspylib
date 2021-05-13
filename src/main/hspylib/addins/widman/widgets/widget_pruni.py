import re

from hspylib.core.tools.commons import sysout

from hspylib.addins.widman.widget import Widget
from hspylib.modules.cli.icons.font_awesome.widget_icons import WidgetIcons


class WidgetPruni(Widget):

    def __init__(self):
        super().__init__(WidgetIcons.PRUNI, "Pruni", (0, 1, 0), "Print a backslash 4 digits unicode character")

    def execute(self):
        print('TODO Finish implementing')
        str_code = '\uFA9E'
        if not re.match(r"^[a-fA-F0-9]{4}$", str_code):
            sysout(self.usage())
        else:
            sysout('\\u{}'.format(str_code))

    def cleanup(self):
        pass
