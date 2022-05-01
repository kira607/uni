class PictureCreator:
    @staticmethod
    def get_picture(
        image='picture',
        caption='picture',
        label='picture',
        attrs='H',
        pos='\\centering',
        width='0.7\\linewidth',
    ) -> str:
        return (
            f'\\begin{{figure}}[{attrs}]\n'
            f'    {pos}\n'
            f'    \\includegraphics[width={width}]{{photo/{image}}}\n'
            f'    \\caption{{{caption}}}\n'
            f'    \\label{{fig:{label}}}\n'
            f'\\end{{figure}}\n'
        )