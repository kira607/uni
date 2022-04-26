class TableCreator:
    def __init__(self, rows, strip=False, strip_n=0, cols_type='c'):
        self.strip = strip
        self.strip_n = strip_n
        self.rows = rows
        self.cols_type = cols_type
        if self.strip:
            self.strip_rows()
        self.cols_num = len(rows[0]) if not strip else strip_n
        self.validate_rows()

    def get_table(self):
        self.validate_rows()
        cols_string = self.get_cols_string()
        data = '\\hline'
        for row in self.rows:
            data += '\n' + '        ' + ' & '.join(row) + ' \\\\ \n        \\hline'
        t = rf'''
\begin{{table}}[H]
    \centering
    \begin{{tabular}}{{{cols_string}}}
        {data}
    \end{{tabular}}
\end{{table}}
        '''
        return t

    def get_cols_string(self):
        s = f"|{'|'.join([self.cols_type for _ in range(self.cols_num)])}|"

    def validate_rows(self) -> None:
        '''
        Check if each row has the same number of columns and each item in rows are strings
        '''
        for i, row in enumerate(self.rows):
            if len(row) != self.cols_num:
                raise RuntimeError(f'Row {i} has {len(row)} elements, but number of columns is {self.cols_num}')
            for index, item in enumerate(row):
                if not isinstance(item, str):
                    try:
                        self.rows[i][index] = str(item)
                    except Exception:
                        raise RuntimeError(f'Row {i}, element {index}: Cannot cast item to a string')

    def strip_rows(self):
        nrows = []
        to_strip = self.strip_n
        if len(self.rows) % to_strip != 0:
            raise RuntimeError(f'Error: {len(self.rows)} % {to_strip} = {len(self.rows) % to_strip}')
        row = []
        for i, d in enumerate(self.rows):
            if i == 0 or i % to_strip == 0:
                if i != 0:
                    nrows.append(row)
                row = []
            row.append(d)

        self.rows = nrows
        self.strip = False
