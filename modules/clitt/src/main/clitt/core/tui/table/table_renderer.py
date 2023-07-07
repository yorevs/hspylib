#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: clitt.core.tui.table
      @file: table_renderer.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.term.terminal import Terminal
from clitt.core.tui.table.table_enums import TextAlignment, TextCase
from hspylib.core.preconditions import check_argument
from hspylib.core.tools.commons import file_is_not_empty
from hspylib.core.tools.text_tools import elide_text, ensure_endswith
from typing import Any, Callable, Iterable, List

import csv
import os


class TableRenderer:
    """Utility class to render terminal UI tables."""

    DEFAULT_MINIMUM_CELL_SIZE = 6

    @staticmethod
    def import_csv(
        filepath: str, caption: str | None = None, has_headers: bool = True, delimiter: chr = ","
    ) -> "TableRenderer":
        """Render the table based on a CSV file."""
        check_argument(file_is_not_empty(filepath), f"File not found: {filepath}")
        headers, data = None, []
        with open(filepath, encoding="UTF8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=delimiter)
            line_count = 0
            for row in csv_reader:
                line_count += 1
                if line_count == 1:
                    if has_headers:
                        headers = row
                        continue
                    headers = [f"C{idx}" for idx, _ in enumerate(row)]
                data.append(row)
        return TableRenderer(headers, data, caption)

    def __init__(self, headers: List[str], data: Iterable, caption: str | None = None):
        """
        :param headers: table headers to be displayed.
        :param data: table record set with the selected rows.
        :param caption: table caption to be displayed.
        """

        self._terminal = Terminal.INSTANCE
        self._headers = headers
        self._columns = range(len(self._headers))
        self._data = data if data else []
        self._caption = caption
        self._min_cell_size = self.DEFAULT_MINIMUM_CELL_SIZE
        self._header_alignment = TextAlignment.CENTER
        self._cell_alignment: TextAlignment = TextAlignment.LEFT
        self._header_case: TextCase = TextCase.UPPER
        check_argument(len(self._headers) >= 1, "Headers are required")
        if data:
            check_argument(
                len(min(data, key=len)) == len(self._headers),
                "Headers and Columns must have the same size: {} vs {}",
                len(min(data, key=len)),
                len(self._headers),
            )
        self._column_sizes = None
        self.adjust_auto_fit()

    @property
    def terminal(self) -> Terminal:
        return self._terminal

    @property
    def data(self) -> Iterable:
        return self._data

    @property
    def cell_alignment(self) -> Callable:
        return self._cell_alignment.val()

    @property
    def header_alignment(self) -> Callable:
        return self._header_alignment.val()

    @property
    def header_case(self) -> Callable:
        return self._header_case.val()

    def set_header_alignment(self, alignment: TextAlignment) -> None:
        """Set table headers alignment.
        :param alignment: table header text alignment function.
        :return:
        """
        self._header_alignment = alignment

    def set_header_case(self, test_case: TextCase) -> None:
        """Set table headers alignment.
        :param test_case: table header text case function.
        :return:
        """
        self._header_case = test_case

    def set_cell_alignment(self, alignment: TextAlignment) -> None:
        """Set table cell alignment.
        :param alignment: table cell text alignment function.
        :return:
        """
        self._cell_alignment = alignment

    def set_cell_sizes(self, *cell_sizes) -> None:
        """Render table based on a list of fixed sizes.
        :param cell_sizes: the list of specific cell sizes.
        :return: None
        """
        for idx, size in enumerate(cell_sizes[: len(self._column_sizes)]):
            self._column_sizes[idx] = max(self._min_cell_size, size)

    def set_min_cell_size(self, size: int) -> None:
        """Set the minimum length of a cell.
        :param size: minimum table cell size.
        :return:
        """
        self._min_cell_size = max(self.DEFAULT_MINIMUM_CELL_SIZE, size)
        self.set_cell_sizes(*(max(self._column_sizes[idx], size) for idx, _ in enumerate(self._headers)))

    def adjust_cells_by_headers(self) -> None:
        """Adjust cell sizes based on the column header length.
        :return: None
        """
        self.set_cell_sizes(*(max(self._min_cell_size, len(header)) for header in self._headers))

    def adjust_cells_by_largest_header(self) -> None:
        """Adjust cell sizes based on the maximum length of a header.
        :return: None
        """
        max_len = len(max(self._headers))
        self.set_cell_sizes(*(max(self._min_cell_size, max_len) for _ in self._headers))

    def adjust_cells_by_largest_cell(self) -> None:
        """Adjust cell sizes based on the maximum length of a cell.
        :return: None
        """
        max_len = 0
        for row in self._data:
            max_len = max(max_len, len(max(list(map(str, row)), key=len)))
        self.set_cell_sizes(*(max_len for _ in self._headers))

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
        for row in self._data:
            max_len = max(max_len, len(max(list(map(str, row)), key=len)))
        self._column_sizes = [max(max_len, len(header)) for header in self._headers]

    def render(self) -> None:
        """Render the table.
        :return: None
        """
        header_line, data_lines = self._format_header_row(), self._format_data_rows()
        table_line = "+" + "+".join(f"{'-' * (self._column_sizes[idx] + 2)}" for idx in self._columns) + "+"
        self._render_table(table_line, header_line, data_lines)

    def export_csv(self, filepath: str, delimiter: chr = ",", has_headers: bool = True) -> None:
        """Export the table to CSV format."""
        csv_file = ensure_endswith(filepath, ".csv")
        with open(csv_file, "w", encoding="UTF8") as csv_file:
            writer = csv.writer(csv_file, delimiter=delimiter)
            if has_headers:
                writer.writerow(self._headers)
            writer.writerows(self._data)

    def _display_data(self, data: Any) -> None:
        """Print out data into the screen."""
        self.terminal.cursor.writeln(data)

    def _format_header_row(self) -> str:
        """Format the table header using the defined preferences."""
        header_cols = [self.header_alignment(self._header_text(idx), self._column_sizes[idx]) for idx in self._columns]
        return f"| {' | '.join(header_cols)} |"

    def _format_data_rows(self) -> List[str]:
        """Format the table rows using the defined preferences."""
        # fmt: off
        return [
            "| " +
                ' | '.join(
                    f"{self.cell_alignment(self._cell_text(row, column), self._column_sizes[column])}"
                    for column in self._columns
                ) +
            " |" for row in self._data
        ]
        # fmt: on

    def _header_text(self, column: int) -> str:
        """Return a header for the specified column.
        :param column the specified table column.
        """
        return self.header_case(elide_text(self._headers[column], self._cell_size(column)))

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
        if self._caption:
            border_line = render_line.replace("+", "-")
            self._display_data(border_line)
            self._display_data(f"| {elide_text(self._caption, line_length): ^{line_length}} |")
        self._display_data(render_line)
        self._display_data(header_row)
        self._display_data(render_line)
        self._display_data(f"{os.linesep.join(data_rows) if data_rows else empty_line}")
        self._display_data(render_line)
