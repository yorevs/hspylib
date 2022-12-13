#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.table
      @file: table_renderer.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from abc import ABC
from hspylib.core.preconditions import check_argument
from hspylib.core.tools.text_tools import elide_text, justified_center, justified_left, justified_right
from typing import List, Optional

import sys


class TableRenderer:
    """TODO"""

    # pylint: disable=too-few-public-methods
    class TextAlignment(ABC):
        """
        Table cell text justification helper.
        """

        LEFT = justified_left
        CENTER = justified_center
        RIGHT = justified_right

    def __init__(self, table_headers: List[str], table_data: Optional[iter], table_caption: str = None):
        """
        :param table_headers: table headers to be displayed.
        :param table_data: table record set with the selected rows.
        :param table_caption: table caption to be displayed.
        """

        self.headers = table_headers
        self.rows = table_data if table_data else []
        self.caption = table_caption
        self.header_alignment = TableRenderer.TextAlignment.CENTER
        self.cell_alignment = TableRenderer.TextAlignment.LEFT
        self.min_column_size = 6
        if self.rows:
            check_argument(
                len(min(self.rows, key=len)) == len(self.headers),
                "Headers and Columns must have the same size: {} vs {}",
                len(min(self.rows, key=len)),
                len(self.headers),
            )
        self.column_sizes = [max(self.min_column_size, len(header)) for header in self.headers]
        self.indexes = range(len(self.column_sizes))

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
        check_argument(
            len(min(self.rows, key=len)) == len(cell_sizes),
            "Sizes and Columns must have the same size: {} vs {}",
            len(min(self.rows, key=len)),
            len(cell_sizes),
        )
        for row in self.rows:
            for idx in range(0, len(row)):
                self.column_sizes[idx] = max(cell_sizes[idx], self.min_column_size)

    def render(self, file=sys.stdout) -> None:
        """
        Render table based on the maximum size of a column header.
        :param file: a file-like object (stream); defaults to the current sys.stdout.
        :return: None
        """
        header_cols, data_cols = self._join_header_columns(), self._join_data_columns()
        table_borders = "+" + "".join((("-" * (self.column_sizes[idx] + 2) + "+") for idx in self.indexes))
        self._print_table(table_borders, header_cols, data_cols, file)

    def _join_header_columns(self) -> list:
        """TODO"""
        cols = [self.header_alignment(self._header_text(idx), self.column_sizes[idx]) for idx in self.indexes]
        return ["| " + " | ".join(cols) + " |"]

    # pylint: disable=consider-using-f-string
    def _join_data_columns(self) -> list:
        """TODO"""
        return [
            "| "
            + "".join(
                "%s | " % self.cell_alignment(self._cell_text(row, idx), self.column_sizes[idx]) for idx in self.indexes
            )
            for row in self.rows
        ]

    def _header_text(self, idx: int) -> str:
        """TODO"""
        return elide_text(self.headers[idx], self._cell_size(idx))

    def _cell_text(self, row: tuple, idx: int) -> str:
        """TODO"""
        return elide_text(str(row[idx]), self._cell_size(idx))

    def _cell_size(self, idx: int) -> int:
        """TODO"""
        return self.column_sizes[idx]

    def _print_table(self, table_line: str, header_cols: List[str], data_cols: List[str], file=sys.stdout) -> None:
        """TODO"""

        if self.caption:
            print(table_line.replace("+", "-"), file=file)
            print(
                "| " + elide_text(self.caption, len(table_line) - 4).center(len(header_cols[0]) - 4, " ") + " |",
                file=file,
            )
        print(f"|{table_line[1:-1]}|", file=file)
        print("\n".join(header_cols), file=file)
        print(f"|{table_line[1:-1]}|", file=file)
        print(
            "\n".join(data_cols) if data_cols else "| " + "<empty>".center(len(table_line) - 4, " ") + " |", file=file
        )
        print(table_line.replace("+", "-"), file=file)
