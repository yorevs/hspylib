#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.tables
      @file: table_renderer.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import sys
from typing import List, Optional

from hspylib.core.tools.text_helper import TextAlignment, fit_text


class TableRenderer:
    
    def __init__(
            self,
            table_headers: List[str],
            table_data: Optional[iter],
            table_caption: str = None):
        """
        :param table_headers: table headers to be displayed.
        :param table_data: table record set with the selected rows.
        :param table_caption: table caption to be displayed.
        """
        self.headers = table_headers
        self.rows = table_data if table_data else []
        self.caption = table_caption
        self.header_alignment = TextAlignment.CENTER
        self.cell_alignment = TextAlignment.LEFT
        self.min_column_size = 6
        if self.rows:
            assert len(min(self.rows, key=len)) == len(self.headers), \
                f'Headers and Columns must have the same size: {len(min(self.rows, key=len))} vs {len(self.headers)}'
        self.column_sizes = [
            max(self.min_column_size, len(header)) for header in self.headers
        ]
        self.indexes = range(0, len(self.column_sizes))
    
    def set_header_alignment(self, alignment: TextAlignment) -> None:
        """
        Set table header justification.
        :param alignment: table header text alignment function.
        :return:
        """
        self.header_alignment = alignment
    
    def set_cell_alignment(self, alignment: TextAlignment) -> None:
        """
        Set table header justification.
        :param alignment: table cell text alignment function.
        :return:
        """
        self.cell_alignment = alignment
    
    def set_min_column_size(self, size: int) -> None:
        """
        Set table header justification.
        :param size: minimum table cell size.
        :return:
        """
        self.min_column_size = size
    
    def adjust_sizes_by_largest_cell(self) -> None:
        """
        Render table based on the maximum size of all cell data.
        :return: None
        """
        for row in self.rows:
            for idx, dummy in enumerate(row):
                self.column_sizes[idx] = max(self.column_sizes[idx], len(str(row[idx])))
    
    def set_fixed_cell_size(self, width: int) -> None:
        """
        Render table based on a fixed size for all cell data.
        :return: None
        """
        for row in self.rows:
            for idx in range(0, len(row)):
                self.column_sizes[idx] = max(width, self.min_column_size)
    
    def set_cell_sizes(self, cell_sizes: List[int]) -> None:
        """
        Render table based on a list of fixed sizes.
        :return: None
        """
        assert len(min(self.rows, key=len)) == len(cell_sizes), \
            f'Sizes and Columns must have the same size: {len(min(self.rows, key=len))} vs {len(cell_sizes)}'
        for row in self.rows:
            for idx in range(0, len(row)):
                self.column_sizes[idx] = max(cell_sizes[idx], self.min_column_size)
    
    def render(self, file=sys.stdout) -> None:
        """
        Render table based on the maximum size of a column header.
        :param file: a file-like object (stream); defaults to the current sys.stdout.
        :return: None
        """
        header_cols = self.__join_header_columns()
        data_cols = self.__join_data_columns()
        table_borders = '+' + ''.join((('-' * (self.column_sizes[idx] + 2) + '+') for idx in self.indexes))
        self.__print_table(table_borders, header_cols, data_cols, file)
    
    def __join_header_columns(self) -> list:
        cols = [self.header_alignment(self.__header_text(idx), self.column_sizes[idx]) for idx in self.indexes]
        return ['| ' + ' | '.join(cols) + ' |']
    
    def __join_data_columns(self) -> list:
        return [
            '| ' + ''.join(
                '%s | ' % self.cell_alignment(self.__cell_text(row, idx), self.column_sizes[idx]) for idx
                in self.indexes
            ) for row in self.rows
        ]
    
    def __header_text(self, idx: int) -> str:
        return fit_text(self.headers[idx], self.__cell_size(idx))
    
    def __cell_text(self, row: tuple, idx: int) -> str:
        return fit_text(str(row[idx]), self.__cell_size(idx))
    
    def __cell_size(self, idx: int) -> int:
        return self.column_sizes[idx]
    
    def __print_table(
            self,
            table_line: str,
            header_cols: List[str],
            data_cols: List[str],
            file=sys.stdout) -> None:
        if self.caption:
            print(table_line, file=file)
            print('| ' + fit_text(self.caption, len(table_line) - 4)
                  .center(len(header_cols[0]) - 4, ' ') + ' |', file=file)
        print(table_line, file=file)
        print('\n'.join(header_cols), file=file)
        print(table_line, file=file)
        print(
            '\n'.join(data_cols) if data_cols
            else '| ' + '<empty>'.center(len(table_line) - 4, ' ') + ' |', file=file
        )
        print(table_line, file=file)
