import os
from ._config import Config
from distutils.dir_util import copy_tree


class Creator:
    def __init__(self, config: Config):
        self.config = config
        self.report_dir = self.get_report_dir()
        self.has_num = '1' if self.config.num else '0'
        self.has_partners = '1' if self.config.partners else '0'

    def run(self):
        self.create_reprot_files()
        self.replace_main_report_file()
        self.replace_title_page_file()
        self.create_chapters()

    def create_reprot_files(self):
        template_path = os.path.join(os.getcwd(), 'report_creator', self.config.template_path)
        copy_tree(template_path, self.report_dir)

    def replace_main_report_file(self):
        path = f'{self.report_dir}/modules/title_page.tex'
        with open(path, 'w', encoding='utf-8') as f:
            tw = self.get_title_page()  # to write
            f.write(tw)

    def replace_title_page_file(self):
        path = f'{self.report_dir}/{self.config.report_name}.tex'
        with open(path, 'w', encoding='utf-8') as f:
            tw = self.get_main_reprot_file()  # to write
            f.write(tw)

    def create_chapters(self):
        for i, chapter_item in enumerate(self.config.chapters.items(), 1):
            chapter, content = chapter_item
            chapter_file_name = self.get_chapter_name(i, chapter)
            chapter_file_path = f'{self.report_dir}/modules/chapters/{chapter_file_name}.tex'
            self._touch(chapter_file_path)
            with open(chapter_file_path, 'w', encoding='utf-8') as f:
                chapter_content = f'{self.config.sectioning}{{{content}}}' if not content.startswith('#') else content[1:]
                f.write(chapter_content)

    def get_report_dir(self):
        root = os.getcwd()
        print(f'running from: {root}')
        print(f'dest: {self.config.dest_path}')
        print(f'dir: {self.config.dir_name}')
        report_dir = os.path.join(root, self.config.dest_path, self.config.dir_name)
        print(f'report_dir: {report_dir}')
        return report_dir

    def get_main_reprot_file(self):
        chapters_section = self.get_chapters_section()
        title_page_content = self.get_main_page_content(chapters_section)
        return title_page_content

    def _touch(self, file_name: str):
        try:
            os.utime(file_name, None)
        except OSError:
            open(file_name, 'a').close()

    def get_chapters_section(self):
        chapters_section = ""
        for i, chapter in enumerate(self.config.chapters, 1):
            chapters_section += f'    \\input{{modules/chapters/{self.get_chapter_name(i, chapter)}.tex}}'
            if i < len(self.config.chapters):
                chapters_section += '\n'
                if self.config.newpage:
                    chapters_section += '\n    \\newpage\n\n'

        return chapters_section

    def get_main_page_content(self, chapters_section):
        main_page_content = f'''\\newcommand{{\\department}}{{{self.config.department}}}
\\newcommand{{\\lablabel}}{{{self.config.label}}}
\\newcommand{{\\hasnum}}{{{self.has_num}}}
\\newcommand{{\\labnum}}{{{self.config.num}}}
\\newcommand{{\\discipline}}{{{self.config.discipline}}}
\\newcommand{{\\theme}}{{{self.config.theme}}}
\\newcommand{{\\haspartners}}{{{self.has_partners}}}
% partners: {', '.join(self.config.partners) if self.has_partners == '1' else 'None'}
\\newcommand{{\\teachername}}{{{self.config.teacher}}}
\\newcommand{{\\labyear}}{{{self.config.year}}}

\\input{{modules/preamble.tex}}

\\begin{{document}}

    \\input{{modules/title_page.tex}}

{chapters_section}

\\end{{document}}
'''
        return main_page_content

    def get_title_page(self):
        partners = self.get_partners()
        title_page = f'''\\thispagestyle{{empty}}

\\begin{{center}}
    \\Large{{
            \\textbf{{МИНОБРНАУКИ РОССИИ}}

            \\textbf{{Санкт-Петербургский государственный}}

            \\textbf{{электротехнический университет «ЛЭТИ»}}

            \\textbf{{им. В.И. Ульянова (Ленина)}}

            \\textbf{{Кафедра \\department}}
    }}
\\end{{center}}

\\topskip=0pt
\\vspace*{{\\fill}}

\\begin{{center}}
    \\Large{{
            \\textbf{{
                    \\lablabel 
                        \\if \\hasnum 1 
                        №\\labnum 
                        \\fi
                        \\\\
                    по дисциплине «\\discipline»\\\\
                    Тема: \\theme\\\\
            }}
    }}
\\end{{center}}

\\vspace*{{\\fill}}

\\begin{{tabular}}{{lcr}}
    Студент\\if \\haspartners 1ы \\fi\\ гр. 9892 & \\begin{{tabular}}{{p{{60mm}}}} \\\\ \\hline \\end{{tabular}} & Лескин К.А.  \\\\\\\\
{partners}
    Преподаватель     & \\begin{{tabular}}{{p{{60mm}}}} \\\\ \\hline \\end{{tabular}} & \\teachername \\\\\\\\
\\end{{tabular}}

\\begin{{center}}
    Санкт-Петербург\\\\
    \\labyear
\\end{{center}}

\\newpage'''

        return title_page

    def get_partners(self):
        partners = ''
        if not self.config.partners:
            return partners
        for partner in self.config.partners:
            partners += (
                f'                      & '
                f'\\begin{{tabular}}{{p{{60mm}}}} \\\\ \\hline \\end{{tabular}} & {partner} \\\\\\\\\n'
            )
        return partners

    def get_chapter_name(self, i, chapter):
        return f'{i}-{chapter}' if not chapter.startswith('#') else chapter[1:]
