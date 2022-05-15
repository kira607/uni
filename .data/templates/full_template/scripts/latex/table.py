class Cell:
    def __init__(self, value: str):
        self.value = str(value)

    def render(self) -> str:
        result = self.value
        return result


class Row:
    def __init__(self, cols: int):
        self._cols = cols
        self._cells = []

    def __iter__(self):
        return iter(self._cells)

    def __getitem__(self, key):
        return self._cells[key]

    def set(self, *cells: str):
        if len(cells) != self._cols:
            raise ValueError(f'Too {"much" if len(cells) < self._cols else "few"} values for row!')
        for cell_val in cells:
            cell = Cell(cell_val)
            self._cells.append(cell)

    def render(self) -> str:
        result = ' & '.join(cell.render() for cell in self._cells)
        result += ' \\\\\n'
        return result


class Header(Row):
    pass


class LatexTable:
    '''A class for creating a latex table.'''

    def __init__(
        self, 
        cols_num: int,
        cols_type: str = 'c',
        pos: str = '\\centering',
        caption: str = None,
        caption_pos: str = 'top',
        label: str = None,
    ) -> None:
        self.cols_num = cols_num
        self._header = None
        self._rows = []
        self._cols_string = self.get_cols_string(cols_type)
        self._pos = pos
        self._caption_pos = caption_pos if caption_pos in ('top', 'bottom') else 'top'
        self._caption = f'\n    \\caption{{{caption}}}' if caption else ''
        self._label = f'\n    \\label{{tab:{label}}}' if label else ''

    def set_header(self, *cells) -> None:
        self._header = Header(self.cols_num)
        self._header.set(*cells)

    def add_row(self, *cells: str):
        new_row = Row(self.cols_num)
        new_row.set(*cells)
        self._rows.append(new_row)

    def render(self) -> str:
        indent = ' ' * 8
        data = '\\hline'

        if self._header:
            data += f'\n{indent}{self._header.render()}{indent}\\hline'
        
        for row in self._rows:
            data += f'\n{indent}{row.render()}{indent}\\hline'
        t = rf'''
\begin{{table}}[H]
    {self._pos}{self._caption if self._caption_pos == "top" else ""}
    \begin{{tabular}}{{{self._cols_string}}}
        {data}
    \end{{tabular}}{self._caption if self._caption_pos == "bottom" else ""}{self._label}
\end{{table}}
        '''
        return t

    def get_cols_string(self, cols_type: str) -> str:
        if cols_type not in 'lcr' or len(cols_type) != 1:
            cols_type = 'c'
        cols_string = f"|{'|'.join([cols_type for _ in range(self.cols_num)])}|"
        return cols_string

    def list_to_rows(self, l: list, n: int = None) -> tuple:
        '''
        Split one list into a list of rows.

        Example::

            >>> LatexTable(2).list_to_rows([1, 2, 3, 4, 5, 6, 7, 8])
            ([1, 2], [3, 4], [5, 6], [7, 8])
        '''
        n = n or self.cols_num
        if len(l) % n != 0:
            raise RuntimeError(
                f'Error: the list contains the number of elements '
                f'which cannot be stipped into a {n} number of columns. '
                f'({len(l)} % {n} = {len(l) % n} extra elements)'
            )
        return tuple(l[i:j] for i, j in zip(range(0, len(l) + 1, n), range(n, len(l) + 1, n)))
