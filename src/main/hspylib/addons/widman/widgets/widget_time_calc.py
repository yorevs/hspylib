import math
import re

from hspylib.addons.widman.widget import Widget
from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.icons.font_awesome.widget_icons import WidgetIcons


class WidgetTimeCalc(Widget):

    WIDGET_ICON  = WidgetIcons.TCALC
    WIDGET_NAME = "TimeCalc"
    TOOLTIP = "Calculate time based operations"
    USAGE = "Usage: TimeCalc [-d|--decimal] <HH1:MM1[:SS1]> <+|-> <HH2:MM2[:SS2]>"
    VERSION = (0, 1, 0)

    def __init__(self):
        super().__init__(
            WidgetTimeCalc.WIDGET_ICON,
            WidgetTimeCalc.WIDGET_NAME,
            WidgetTimeCalc.TOOLTIP,
            WidgetTimeCalc.USAGE,
            WidgetTimeCalc.VERSION)

        self.total_seconds = 0
        self.op = '+'
        self.decimal = False

    def execute(self, *args):
        if (not args or len(args) < 3) and not any(a in args for a in ['-h', '--help']):
            if not self._read_args():
                return
        elif args[0] in ['-h', '--help']:
            sysout(self.usage())
            return
        elif args[0] in ['-d', '--decimal']:
            self.decimal = True
            args = args[1:]

        for tm in args:
            if re.match(r"[+-]", tm):
                self.op = tm
            elif re.match(r"^([0-9]{1,2}:?)+", tm):
                try:
                    parts = [int(math.floor(float(s))) for s in tm.split(':')]
                except ValueError:
                    parts = [0, 0, 0]
                f_hours = parts[0] if len(parts) > 0 else 0
                f_minutes = parts[1] if len(parts) > 1 else 0
                f_secs = parts[2] if len(parts) > 2 else 0
                tm_amount = ((f_hours * 60 + f_minutes) * 60 + f_secs)

                if self.op == '+':
                    self.total_seconds += tm_amount
                elif self.op == '-':
                    self.total_seconds -= tm_amount

        self.total_seconds, seconds = divmod(self.total_seconds, 60)
        hours, minutes = divmod(self.total_seconds, 60)

        if self.decimal:
            sysout(f"{hours:02d}.{self._decimal(minutes):02d}.{self._decimal(seconds):02d}")
        else:
            sysout(f"{hours:02d}:{self._decimal(minutes):02d}:{self._decimal(seconds):02d}")

    def cleanup(self):
        pass

    # @purpose: Convert a raw time into decimal
    def _decimal(self, time_raw: int = 0) -> int:
        return int(round(((time_raw / 60.00) * 100.00) if self.decimal else time_raw))

    def _read_args(self) -> bool:
        return False
