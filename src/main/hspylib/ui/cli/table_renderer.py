import sys
from typing import List, Optional, Callable

from hspylib.core.tools.text_helper import TextStyle, TextAlignment

MIN_COL_LENGTH = 6


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
        self.data = table_data
        self.caption = table_caption
        self.header_alignment = TextAlignment.CENTER
        self.cell_alignment = TextAlignment.LEFT
        self.rows = [r for r in self.data] if self.data else []
        self.column_sizes = None
        self.indexes = None

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

    def render(self, file=sys.stdout) -> None:
        """
        Render table based on the maximum length between a column data and header. Data will not be wrapped.
        :param file: a file-like object (stream); defaults to the current sys.stdout.
        :return: None
        """
        if self.rows:
            assert len(min(self.rows, key=len)) == len(self.headers), \
                f'Headers and Columns must have the same size: {len(min(self.rows, key=len))} vs {len(self.headers)}'
        self.column_sizes = [max(MIN_COL_LENGTH, len(header)) for header in self.headers]
        self.indexes = range(0, len(self.column_sizes))
        for row in self.rows:
            for idx in range(0, len(row)):
                self.column_sizes[idx] = max(self.column_sizes[idx], len(str(row[idx])))
        header_cols = self.__join_header_columns()
        data_cols = self.__join_data_columns()
        table_borders = '+' + ''.join((('-' * (self.column_sizes[idx] + 2) + '+') for idx in self.indexes))
        self.__print_table(table_borders, header_cols, data_cols, file)

    def __join_header_columns(self) -> list:
        cols = [self.header_alignment(self.headers[idx], self.column_sizes[idx]) for idx in self.indexes]
        return ['| ' + ' | '.join(cols) + ' |']

    def __join_data_columns(self) -> list:
        return [
            '| ' +
            ''.join('%s | ' % self.cell_alignment(str(row[idx]), self.column_sizes[idx]) for idx in self.indexes) for row in self.rows
        ]

    def __print_table(
            self,
            table_line: str,
            header_cols: List[str],
            data_cols: List[str],
            file=sys.stdout) -> None:
        """
        Print the table to stdout or to a file.
        :param table_line: table border lines
        :param header_cols: table table_headers to be displayed.
        :param data_cols: table data to be displayed.
        :param file: a file-like object (stream); defaults to the current sys.stdout.
        :return: None
        """
        if self.caption:
            print(table_line, file=file)
            print('| ' + self.caption[0:len(table_line) - 4].center(len(header_cols[0]) - 4, ' ') + ' |', file=file)
        print(table_line, file=file)
        print('\n'.join(header_cols), file=file)
        print(table_line, file=file)
        print(
            '\n'.join(data_cols) if data_cols
            else '| ' + '<empty>'.center(len(table_line) - 4, ' ') + ' |', file=file
        )
        print(table_line, file=file)


if __name__ == '__main__':
    h = [
        'String',
        'Number',
        'Boolean',
        'Thats a big Integer Column Header'
    ]
    data = [
        ('One', 1, True, 2),
        ('Two', 2, False, 3),
        ('Three, four and five', 3, True, 3),
    ]
    tr = TableRenderer(h, data, 'TableRenderer example of usage')
    tr.render()
