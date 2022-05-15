class LatexPicture:
    def __init__(
        self,
        image='picture',
        caption='picture',
        label='picture',
        attrs='H',
        pos='\\centering',
        width='0.7\\linewidth',
    ):
        self.image = image
        self.caption = caption
        self.label = f'fig:{label}'
        self.attrs = attrs
        self.pos = pos
        self.width = width

    def render(self) -> str:
        return (
            f'\\begin{{figure}}[{self.attrs}]\n'
            f'    {self.pos}\n'
            f'    \\includegraphics[width={self.width}]{{photo/{self.image}}}\n'
            f'    \\caption{{{self.caption}}}\n'
            f'    \\label{{{self.label}}}\n'
            f'\\end{{figure}}'
        )