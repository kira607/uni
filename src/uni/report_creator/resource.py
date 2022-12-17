import os
import shutil

from abc import ABC, abstractmethod
from pathlib import Path

from mako.template import Template


class Resource(ABC):
    '''A base resource.'''

    marker = ''

    def __init__(self, path: Path) -> None:
        self.path = path
        self.full_name = self.path.name
        self.name = self._get_name()
        self.children = set()

    def add_sub_resource(self, sub_resource: 'Resource') -> None:
        self.children.add(sub_resource)
    
    def deploy(self, target_directory: Path, **kwargs) -> None:
        self._deploy(target_directory, **kwargs)
        children_dir = self._get_children_dir(target_directory)
        for child in self.children:
            child.deploy(children_dir, **kwargs)

    def _get_name(self) -> str:
        name = self.full_name
        name = name.replace(self.marker, '')
        return name

    def _get_children_dir(self, target_directory: Path) -> Path:
        return Path(target_directory, self.name)

    @abstractmethod
    def _deploy(self, target_directory: Path, **kwargs) -> None:
        raise NotImplementedError()


class FileResource(Resource):
    '''A simple file resource to be copied entirely on deploy.'''

    marker = ''

    def _deploy(self, target_directory: Path, **kwargs) -> None:
        shutil.copy2(str(self.path), str(target_directory))


class TemplateResource(Resource):
    '''A template resource to be populated with data and created as a file.'''

    marker = '.template'

    def _deploy(self, target_directory: Path, **kwargs) -> None:
        with self.path.open('r', encoding='utf8') as f:
            template = Template(f.read())
        rendered = template.render(**kwargs)
        target = Path(target_directory, self.name)
        with open(str(target), 'w', encoding='utf-8') as f:
            f.write(rendered)


class DirectoryResource(Resource):

    marker = ''

    def _deploy(self, target_directory: Path, **kwargs) -> None:
        target = str(Path(target_directory, self.name))
        os.makedirs(target, exist_ok=True)


class IgnoredResource(Resource):

    marker = '.ignore'

    def _deploy(self, target_directory: Path, **kwargs) -> None:
        pass


class ChaptersResource(Resource):

    marker = 'chapters.expand'

    def _deploy(self, target_directory: Path, **kwargs) -> None:
        sectioning = kwargs.pop('sectioning', 'section')
        for i, (name, content) in enumerate(kwargs.items()):
            name = self._get_chapter_name(name, i)
            content = self._get_chapter_content(content, sectioning, i)
            with Path(target_directory, name).open('w') as f:
                f.write(content)

    def _get_chapter_name(self, name: str, i: int) -> str:
        return name.replace('#', str(i))

    def _get_chapter_content(self, content: str, sectioning: str, i: int) -> str:
        return f'\\{sectioning}{{{content.replace("#", str(i))}}}'


class RootResource(DirectoryResource):
    '''
    A directory resource.
    
    Deploys its children at target path, whithout creating a folder.
    '''

    marker = '.resource'

    def _deploy(self, target_directory: Path, **kwargs) -> None:
        pass

    def _get_name(self) -> str:
        return self.full_name

    def _get_children_dir(self, target_directory: Path) -> Path:
        return target_directory


class ResourceCreator:

    _marker_to_resource = tuple(
        (r.marker, r) for r in Resource.__subclasses__() if r.marker
    )
    
    def create_resource(self, target: Path) -> Resource:
        if not target.exists():
            raise RuntimeError(f'Resource at {target} does not exist.')
        
        if str(target).endswith('.ignore'):
            return IgnoredResource(target)
        
        if target.is_dir():
            return self._create_dir_resource(target)
        else:
            return self._create_file_resource(target)

    def _create_file_resource(self, target: Path) -> Resource:
        for marker, resource_cls in self._marker_to_resource:
            if str(target).endswith(marker):
                return resource_cls(target)
        return FileResource(target)

    def _create_dir_resource(self, target: Path) -> Resource:
        if str(target).endswith('.resource'):
            resource = RootResource(target)
        else:
            resource = DirectoryResource(target)
        
        for item in target.iterdir():
            sub = self.create_resource(item)
            resource.add_sub_resource(sub)
        return resource
