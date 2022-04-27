from os import utime
from os.path import abspath, join
from .config import Config
from distutils.dir_util import copy_tree
from mako.template import Template
from uni.locations import data_folder


class Creator:
    def __init__(self, config: Config):
        self.config = config

    def run(self):
        self.copy_template()
        self.write_main_page()
        self.write_title_page()
        self.create_chapters()

    def copy_template(self):
        copy_tree(self.config.template_path, self.config.report_dir)

    def write_main_page(self):
        with open(self.config.main_page_path, 'w', encoding='utf-8') as f:
            tw = self.get_main_page()
            f.write(tw)

    def write_title_page(self):
        with open(self.config.title_page_path, 'w', encoding='utf-8') as f:
            tw = self.get_title_page()
            f.write(tw)

    def create_chapters(self):
        for i, chapter_item in enumerate(self.config.chapters.items(), 1):
            chapter, content = chapter_item
            chapter_file_name = self.get_chapter_name(i, chapter)
            chapter_file_path = abspath(join(self.config.report_dir, 'modules', 'chapters', chapter_file_name))
            self._touch(chapter_file_path)
            with open(chapter_file_path, 'w', encoding='utf-8') as f:
                chapter_content = self.get_chapter_content(content)
                f.write(chapter_content)

    def get_main_page(self):
        path = abspath(join(data_folder, 'files_templates', 'main_file'))
        t = Template(filename=path)
        return t.render(**self.config.dict())

    def get_title_page(self):
        path = abspath(join(data_folder, 'files_templates', 'title_page'))
        t = Template(filename=path)
        return t.render(**self.config.dict())

    def get_chapter_name(self, i, chapter):
        if chapter.startswith('#'):
            name = f'{i}-{chapter[1:]}'
        elif chapter.startswith('\#'):
            name = chapter[1:]
        else:
            name = chapter
        return f'{name}.tex'

    def get_chapter_content(self, content):
        if content.startswith('#'):
            return content[1:]
        else:
            return f'{self.config.sectioning}{{{content}}}'

    def _touch(self, file_name: str):
        try:
            utime(file_name, None)
        except OSError:
            open(file_name, 'a').close()
