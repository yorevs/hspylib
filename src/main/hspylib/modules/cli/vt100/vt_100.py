#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.vt100
      @file: vt_100.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import re
from abc import ABC


class Vt100(ABC):
    """
    References:
        - https://vt100.net/docs/vt100-ug/chapter3.html
        - https://espterm.github.io/docs/VT100%20escape%20codes.html
    """
    
    # Esc<Sequence>
    @classmethod
    def escape(cls, seq: str) -> str:
        return f"\033{seq}"
    
    # Esc[<Code>
    @classmethod
    def sequence(cls, code: str) -> str:
        return cls.escape(f"[{code}")
    
    # Esc7
    @classmethod
    def save_cursor(cls) -> str:
        return cls.escape('7')
    
    # Esc8
    @classmethod
    def restore_cursor(cls) -> str:
        return cls.escape('8')
    
    # Esc[c
    @classmethod
    def reset(cls) -> str:
        return cls.sequence('c')
    
    # Esc[?7<h/l>
    @classmethod
    def set_auto_wrap(cls, enabled: bool) -> str:
        return cls.sequence(f"?7{'h' if enabled else 'l'}")
    
    # Esc[?25<h/l>
    @classmethod
    def set_show_cursor(cls, enabled: bool) -> str:
        return cls.sequence(f"?25{'h' if enabled else 'l'}")
    
    # Esc[<Modes...>m
    @classmethod
    def mode(cls, mod_seq: str) -> str:
        assert re.match(r"[0-9]+(;[0-9]+){0,2}", mod_seq)
        return cls.sequence(f"{mod_seq}m")
    
    # Esc[<n>J
    @classmethod
    def clear_screen(cls, mod_cls: int = None) -> str:
        if mod_cls is None:
            return cls.sequence('J')
        
        assert mod_cls in [0, 1, 2]
        return cls.sequence(f'{mod_cls}J')
    
    # Esc[<n>K
    @classmethod
    def clear_line(cls, mod_cls: int = None) -> str:
        if mod_cls is None:
            return cls.sequence('K')
        
        assert mod_cls in [0, 1, 2]
        return cls.sequence(f'{mod_cls}K')
    
    # Esc[<v>;<h>H
    @classmethod
    def cursor_pos(cls, cup_seq: str = None) -> str:
        if cup_seq is None:
            return cls.sequence('H')
        
        assert re.match(r"[0-9]*;[0-9]*", cup_seq)
        return cls.sequence(f"{cup_seq}H")
    
    # Esc[<n><A/B/C/D>
    @classmethod
    def cursor_move(cls, amount: int, direction: str) -> str:
        assert int(amount) >= 0 and direction in ['A', 'B', 'C', 'D']
        return cls.sequence(f"{amount}{direction}")
    
    # Esc[<n>A
    @classmethod
    def cursor_move_up(cls, amount: int = None) -> str:
        return cls.cursor_move(amount if amount else 0, 'A')
    
    # Esc[<n>B
    @classmethod
    def cursor_move_down(cls, amount: int = None) -> str:
        return cls.cursor_move(amount if amount else 0, 'B')
    
    # Esc[<n>C
    @classmethod
    def cursor_move_forward(cls, amount: int = None) -> str:
        return cls.cursor_move(amount if amount else 0, 'C')
    
    # Esc[<n>D
    @classmethod
    def cursor_move_backward(cls, amount: int = None) -> str:
        return cls.cursor_move(amount if amount else 0, 'D')
