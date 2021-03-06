import re
import signal
from abc import ABC
from typing import List, Any

from hspylib.core.tools.keyboard import Keyboard
from hspylib.ui.cli.vt100.vt_100 import Vt100

from hspylib.ui.cli.vt100.vt_codes import vt_print

from hspylib.core.tools.commons import sysout, screen_size
from hspylib.ui.cli.menu.menu_utils import MenuUtils
from hspylib.ui.cli.vt100.vt_colors import VtColors


def mchoose(all_options: List[Any], checked: bool = True) -> List[Any]:
    """
    TODO
    :param all_options:
    :param checked:
    :return:
    """
    return MenuChoose.choose(all_options, checked)


class MenuChoose(ABC):

    @classmethod
    def choose(
            cls,
            items: List[Any],
            checked: bool = True,
            title: str = 'Please select one',
            max_rows: int = 15,
            title_color: VtColors = VtColors.ORANGE,
            highlight_color: VtColors = VtColors.BLUE,
            nav_color: VtColors = VtColors.YELLOW) -> List[Any]:

        done = None
        show_from = 0
        re_render = 1
        sel_options = []
        length = len(items)
        signal.signal(signal.SIGINT, MenuUtils.exit_app)

        if length > 0:
            sel_index = 0
            init_value = 1 if checked else 0
            show_to = max_rows - 1

            diff_index = show_to - show_from
            length = len(items)

            # Initialize all options
            sel_options = [init_value for _ in range(length)]

            sysout(f"%ED2%%HOM%{title_color.placeholder()}{title}")
            vt_print(Vt100.set_auto_wrap(False))
            vt_print('%HOM%%CUD(1)%%ED0%')
            vt_print(Vt100.save_cursor())

            # Wait for user interaction
            while not done:

                # Menu Renderization {
                if re_render:
                    cls.__render__(items, sel_options, show_from, show_to, sel_index, highlight_color)
                    sysout(
                        f"{nav_color.placeholder()} [Enter] Accept  [\u2191\u2193] Navigate  [Space] Mark  [Q] Quit  [1..{str(length)}] Goto: %EL0%",
                        end='')
                    vt_print(Vt100.set_show_cursor(True))
                    re_render = None
                # } Menu Renderization

                # Navigation input {
                keypress = Keyboard.read_keystroke()
                if keypress == Keyboard.VK_Q or keypress == Keyboard.VK_ESC:
                    done = True
                    sysout('\n%NC%')
                else:
                    if keypress in ['q', 'Q']:  # Exit requested
                        sysout('\n%NC%')
                        break
                    elif keypress.isdigit():  # An index was typed
                        typed_index = keypress.value
                        sysout(f"{keypress.value}", end='')
                        index_len = 1
                        while len(typed_index) < len(str(length)):
                            numpress = Keyboard.read_keystroke()
                            if not numpress:
                                break
                            elif not re.match(r'^[0-9]*$', numpress.value):
                                typed_index = None
                                break
                            typed_index = f"{typed_index}{numpress.value if numpress else ''}"
                            sysout(f"{numpress.value if numpress else ''}", end='')
                            index_len += 1
                        # Erase the index typed by the user
                        sysout(f"%CUB({index_len})%%EL0%", end='')
                        if 1 <= int(typed_index) <= length:
                            show_to = int(typed_index)
                            if show_to <= diff_index:
                                show_to = diff_index
                            show_from = show_to - diff_index
                            sel_index = int(typed_index) - 1
                            re_render = 1
                    elif keypress == Keyboard.VK_SPACE:  # Mark option
                        if sel_options[sel_index] == 0:
                            sel_options[sel_index] = 1
                        else:
                            sel_options[sel_index] = 0
                        re_render = 1
                        continue
                    elif keypress == Keyboard.VK_UP:  # Cursor up
                        if sel_index == show_from and show_from > 0:
                            show_from -= 1
                            show_to -= 1
                        elif sel_index == 0:
                            continue
                        if sel_index - 1 >= 0:
                            sel_index -= 1
                            re_render = 1
                    elif keypress == Keyboard.VK_DOWN:  # Cursor down
                        if sel_index + 1 == show_to and show_to < length:
                            show_from += 1
                            show_to += 1
                        elif sel_index + 1 >= length:
                            continue
                        if sel_index + 1 < length:
                            sel_index += 1
                            re_render = 1
                    elif keypress == Keyboard.VK_ENTER:  # Enter
                        sysout('\n%NC%')
                        break
                # } Navigation input

        return [op for idx, op in enumerate(items) if sel_options[idx] == 1]

    @classmethod
    def __render__(
            cls,
            items: List[Any],
            sel_options: List[int],
            show_from: int,
            show_to: int,
            sel_index: int,
            highlight_color: VtColors = VtColors.BLUE) -> None:

        length = len(items)
        rows, columns = screen_size()
        vt_print(Vt100.set_show_cursor(False))
        # Restore the cursor to the home position
        vt_print(Vt100.restore_cursor())
        sysout('%NC%')

        for idx in range(show_from, show_to):
            selector = ' '
            mark = ' '
            if idx >= length:
                break  # When the number of items is lower than the max_rows, skip the other lines
            option_line = str(items[idx])[0:int(columns)]
            # Erase current line before repaint
            vt_print('%EL2%\r')
            # Print the selector if the index is current
            if idx == sel_index:
                vt_print(highlight_color.code())
                selector = '>'
            # Print the marker if the option is checked
            if sel_options[idx] == 1:
                mark = 'x'
            fmt = " {:>" + str(len(str(length))) + "}  {:>2} [{}] {}"
            sysout(fmt.format(idx + 1, selector, mark, option_line))
            # Check if the text fits the screen and print it, otherwise print '...'
            if len(option_line) >= int(columns):
                vt_print("%CUB(4)%%EL0%...")
                sysout('%NC%')
        sysout('\n')


if __name__ == '__main__':
    it = [f"Item-{n}" for n in range(1, 21)]
    sel = mchoose(it)
    print(str(sel))
