import re

from hspylib.addons.widman.widget import Widget
from hspylib.core.tools.commons import human_readable_bytes
from hspylib.modules.cli.icons.font_awesome.widget_icons import WidgetIcons
from hspylib.modules.cli.vt100.terminal import Terminal


class WidgetFree(Widget):

    WIDGET_ICON  = WidgetIcons.FREE
    WIDGET_NAME = "Free"
    TOOLTIP = "Report system memory usage"
    USAGE = "Usage: Free"
    VERSION = (0, 2, 0)

    def __init__(self):
        super().__init__(
            WidgetFree.WIDGET_ICON,
            WidgetFree.WIDGET_NAME,
            WidgetFree.TOOLTIP,
            WidgetFree.USAGE,
            WidgetFree.VERSION)


    def execute(self, *args):
        # Get process info
        ps = Terminal.shell_exec('ps -caxm -orss,comm')
        vm = Terminal.shell_exec('vm_stat')

        # Iterate processes
        process_lines = ps.split('\n')
        sep = re.compile(' +')
        rss_total = 0  # kB

        for row in range(1, len(process_lines)):
            row_text = process_lines[row].strip()
            row_elements = sep.split(row_text)
            if re.match('^[0-9]+$', row_elements[0]):
                rss = float(row_elements[0]) * 1024
            else:
                rss = 0
            rss_total += rss

        # Process vm_stat
        vm_lines = vm.split('\n')
        sep = re.compile(': +')
        vm_stats = {}

        for row in range(1, len(vm_lines) - 2):
            row_text = vm_lines[row].strip()
            row_elements = sep.split(row_text)
            vm_stats[(row_elements[0])] = int(row_elements[1].strip('\\.')) * 4096

        wired, wu = human_readable_bytes(vm_stats["Pages wired down"])
        active, au = human_readable_bytes(vm_stats["Pages active"])
        inactive, iu = human_readable_bytes(vm_stats["Pages inactive"])
        free, fu = human_readable_bytes(vm_stats["Pages free"])
        real, ru = human_readable_bytes(rss_total)  # Total memory

        print(f"\nReporting system memory usage: \n{'-' * 30}")
        print('    Wired Memory: %06s %s' % (wired, wu))
        print('   Active Memory: %06s %s' % (active, au))
        print(' Inactive Memory: %06s %s' % (inactive, iu))
        print('     Free Memory: %06s %s' % (free, fu))
        print('     Real Memory: %06s %s' % (real, ru))
        print(' ')

    def cleanup(self):
        pass
