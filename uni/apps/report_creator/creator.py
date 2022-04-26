import os
from .config import Config
from distutils.dir_util import copy_tree


class Creator:
    def __init__(self, config: Config):
        self.config = config

    def run(self):
        self.copy_template()
        self.write_main()
        self.write_title_page()
        self.create_chapters()

    def copy_template(self):
        copy_tree(self.config.template_path, self.config.report_dir)

    def write_main(self):
        path = f'{self.config.report_dir}/{self.config.report_name}.tex'
        with open(path, 'w', encoding='utf-8') as f:
            tw = self.get_main_reprot_file()  # to write
            f.write(tw)

    def write_title_page(self):
        path = f'{self.report_dir}/modules/title_page.tex'
        with open(path, 'w', encoding='utf-8') as f:
            tw = self.get_title_page()  # to write
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

    def get_main_reprot_file(self):
        chapters_section = self.get_chapters_section()
        title_page_content = self.get_main_page_content(chapters_section)
        return title_page_content

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
        pass

    def get_title_page(self):
        pass

    def get_chapter_name(self, i, chapter):
        return f'{i}-{chapter}' if not chapter.startswith('#') else chapter[1:]

    def _touch(self, file_name: str):
        try:
            os.utime(file_name, None)
        except OSError:
            open(file_name, 'a').close()
