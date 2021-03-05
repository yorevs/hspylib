import re


class Vt100:
    """
    References:
        - https://vt100.net/docs/vt100-ug/chapter3.html
        - https://espterm.github.io/docs/VT100%20escape%20codes.html
    """

    def __str__(self):
        return self.value

    # Esc<Sequence>
    @staticmethod
    def escape(seq: str) -> str:
        return f"\033{seq}"

    # Esc[<Code>
    @staticmethod
    def sequence(code: str) -> str:
        return Vt100.escape(f"[{code}")

    # Esc[?7<h/l>
    @staticmethod
    def set_auto_wrap(enabled: bool) -> str:
        return Vt100.sequence(f"?7{'h' if enabled else 'l'}")

    # Esc[?25<h/l>
    @staticmethod
    def set_show_cursor(enabled: bool) -> str:
        return Vt100.sequence(f"?25{'h' if enabled else 'l'}")

    # Esc[<Modes...>m
    @staticmethod
    def mode(mod_seq: str) -> str:
        assert re.match(r"[0-9]+(;[0-9]+){0,2}", mod_seq)
        return Vt100.sequence(f"{mod_seq}m")

    # Esc[<n>J
    @staticmethod
    def clear_screen(mod_cls: int = None) -> str:
        if mod_cls is None:
            return Vt100.sequence('J')
        else:
            assert mod_cls in [0, 1, 2]
            return Vt100.sequence(f'{mod_cls}J')

    # Esc[<n>K
    @staticmethod
    def clear_line(mod_cls: int = None) -> str:
        if mod_cls is None:
            return Vt100.sequence('K')
        else:
            assert mod_cls in [0, 1, 2]
            return Vt100.sequence(f'{mod_cls}K')

    # Esc7
    @staticmethod
    def save_cursor():
        return Vt100.escape('7')

    # Esc8
    @staticmethod
    def restore_cursor():
        return Vt100.escape('8')

    # Esc[<v>;<h>H
    @staticmethod
    def cursor_pos(cup_seq: str = None) -> str:
        if cup_seq is None:
            return Vt100.sequence('H')
        else:
            assert re.match(r"[0-9]+;[0-9]+", cup_seq)
            return Vt100.sequence(f"{cup_seq}H")

    # Esc[<n><A/B/C/D>
    @staticmethod
    def cursor_move(amount: int, direction: str) -> str:
        assert int(amount) >= 0 and direction in ['A', 'B', 'C', 'D']
        return Vt100.sequence(f"{amount}{direction}")

    # Esc[<n>A
    @staticmethod
    def cursor_move_up(amount: int = None) -> str:
        return Vt100.cursor_move(amount if amount else 0, 'A')

    # Esc[<n>B
    @staticmethod
    def cursor_move_down(amount: int = None) -> str:
        return Vt100.cursor_move(amount if amount else 0, 'B')

    # Esc[<n>C
    @staticmethod
    def cursor_move_forward(amount: int = None) -> str:
        return Vt100.cursor_move(amount if amount else 0, 'C')

    # Esc[<n>D
    @staticmethod
    def cursor_move_backward(amount: int = None) -> str:
        return Vt100.cursor_move(amount if amount else 0, 'D')
