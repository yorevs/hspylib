#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: clitt.core.tui.table
      @file: table_renderer.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import csv
from typing import Iterable, List

from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.preconditions import check_argument
from hspylib.core.tools.commons import file_is_not_empty, sysout
from hspylib.core.tools.text_tools import elide_text, justified_center, justified_left, justified_right, titlecase


class TableRenderer:
    """Utility class to render terminal UI tables.
    """

    DEFAULT_MINIMUM_CELL_SIZE = 6

    @staticmethod
    def from_csv(
        filepath: str,
        caption: str | None = None,
        delimiter: chr = ',') -> 'TableRenderer':
        """TODO"""

        check_argument(file_is_not_empty(filepath), f"File not found: {filepath}")
        headers, data = None, []
        with open(filepath, encoding="UTF8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=delimiter)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    headers = row
                else:
                    data.append(row)
                line_count += 1
        return TableRenderer(headers, data, caption)

    class TextAlignment(Enumeration):
        """Table cell text justification helper.
        """

        # fmt: off
        LEFT    = justified_left
        CENTER  = justified_center
        RIGHT   = justified_right
        # fmt: on

    def __init__(self, headers: List[str], data: Iterable, caption: str | None = None):
        """
        :param headers: table headers to be displayed.
        :param data: table record set with the selected rows.
        :param caption: table caption to be displayed.
        """

        self._headers = headers
        self._columns = range(len(self._headers))
        self._data = data if data else []
        self._caption = caption or ''
        self._header_alignment = TableRenderer.TextAlignment.CENTER
        self._cell_alignment = TableRenderer.TextAlignment.LEFT
        self._min_cell_size = self.DEFAULT_MINIMUM_CELL_SIZE
        if data:
            check_argument(
                len(min(data, key=len)) == len(self._headers),
                "Headers and Columns must have the same size: {} vs {}",
                len(min(data, key=len)),
                len(self._headers),
            )
        self._column_sizes = [self._min_cell_size for _ in self._headers]

    def set_header_alignment(self, alignment: TextAlignment) -> None:
        """Set table headers alignment.
        :param alignment: table header text alignment function.
        :return:
        """
        self._header_alignment = alignment

    def set_cell_alignment(self, alignment: TextAlignment) -> None:
        """Set table cell alignment.
        :param alignment: table cell text alignment function.
        :return:
        """
        self._cell_alignment = alignment

    def set_min_cell_size(self, size: int) -> None:
        """Set the minimum length of a cell.
        :param size: minimum table cell size.
        :return:
        """
        self._min_cell_size = max(self.DEFAULT_MINIMUM_CELL_SIZE, size)
        self._column_sizes = [max(self._column_sizes[idx], size) for idx, _ in enumerate(self._headers)]

    def set_cell_sizes(self, *cell_sizes) -> None:
        """Render table based on a list of fixed sizes.
        :param cell_sizes: the list of specific cell sizes.
        :return: None
        """
        for idx, size in enumerate(cell_sizes[:len(self._column_sizes)]):
            self._column_sizes[idx] = max(self._min_cell_size, size)

    def adjust_cells_by_headers(self) -> None:
        """Adjust cell sizes based on the column header length.
        :return: None
        """
        self._column_sizes = [max(self._min_cell_size, len(header)) for header in self._headers]

    def adjust_cells_by_largest_header(self) -> None:
        """Adjust cell sizes based on the maximum length of a header.
        :return: None
        """
        max_len = len(max(self._headers))
        self._column_sizes = [max(self._min_cell_size, max_len) for _ in self._headers]

    def adjust_cells_by_largest_cell(self) -> None:
        """Adjust cell sizes based on the maximum length of a cell.
        :return: None
        """
        max_len = 0
        for idx, row in enumerate(self._data):
            max_len = max(max_len, len(max(list(map(str, row)), key=len)))
        self._column_sizes = [max_len for _ in self._headers]

    def adjust_cells_by_fixed_size(self, size: int) -> None:
        """Adjust cell sizes to a fixed size.
        :param size: the fixed cell size.
        :return: None
        """
        self.set_cell_sizes(*(size for _ in self._headers))

    def adjust_auto_fit(self) -> None:
        """Ensure all cells and headers are visible.
        :return: None
        """
        max_len = max(0, int(len(self._caption) / len(self._headers)) - 2)
        for idx, row in enumerate(self._data):
            max_len = max(max_len, len(max(list(map(str, row)), key=len)))
        self._column_sizes = [max(max_len, len(header)) for header in self._headers]

    def render(self) -> None:
        """Render the table.
        :return: None
        """
        header_row, data_rows = self._format_header_row(), self._format_data_rows()
        table_line = "+" + '+'.join(f"{'-' * (self._column_sizes[idx] + 2)}" for idx in self._columns) + '+'
        self._render_table(table_line, header_row, data_rows)

    def to_csv(self, filepath: str) -> None:
        with open(filepath, 'w', encoding="UTF8") as csv_file:
            writer = csv.writer(csv_file,)
            writer.writerow(self._headers)
            writer.writerows(self._data)

    def _format_header_row(self) -> str:
        """Format the table header using the defined preferences.
        """
        header_cols = [
            self._header_alignment(self._header_text(idx), self._column_sizes[idx]) for idx in self._columns
        ]
        return f"| {' | '.join(header_cols)} |"

    def _format_data_rows(self) -> List[str]:
        """Format the table rows using the defined preferences.
        """
        # fmt: off
        return [
            "| " + ' | '.join(
                f"{self._cell_alignment(self._cell_text(row, idx), self._column_sizes[idx])}" for idx in self._columns
            ) + " |" for row in self._data
        ]
        # fmt: on

    def _header_text(self, column: int) -> str:
        """Return a header for the specified column.
        :param column the specified table column.
        """
        return titlecase(elide_text(self._headers[column], self._cell_size(column)), skip_length=1)

    def _cell_text(self, row: tuple, column: int) -> str:
        """Return a text for the specified cell (row, column).
        :param row the specified table row.
        :param column the specified table column.
        """
        return elide_text(str(row[column]), self._cell_size(column))

    def _cell_size(self, column: int) -> int:
        """Return the size of the specified column.
        :param column the specified table column.
        """
        return self._column_sizes[column]

    def _render_table(self, table_line: str, header_row: str, data_rows: List[str]) -> None:
        """Print the table rows and columns.
        :param table_line: a table line formatted using all of the columns.
        :param header_row: the formatted table header row.
        :param data_rows: the formatted table data rows.
        """
        line_length, render_line = len(table_line) - 4, f"+{table_line[1:-1]}+"
        empty_line = f"| {'<empty>': ^{line_length}} |"
        sysout(render_line.replace('+', '-'))
        if self._caption:
            sysout(f"| {elide_text(self._caption, line_length): ^{line_length}} |")
            sysout(render_line)
        sysout(header_row)
        sysout(render_line)
        sysout(f"{'%EOL%'.join(data_rows) if data_rows else empty_line}")
        sysout(render_line.replace('+', '-'))
