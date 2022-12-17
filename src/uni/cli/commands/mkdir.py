from cleo import option, argument

from uni.profile_manager import ProfileManager
from ._command import Command


class MakeProjectDirCommand(Command):
    name = 'mkdir'
    description = 'Create a new project directory.'
    arguments = (
        argument('path', 'where to create a project directory', optional=True, default='.'),
    )
    options = (
        option('university', 'u', 'university of studying', flag=False),
        option('group', 'g', 'studying group.', flag=False),
        option('semnumber', 's', 'semester number', flag=False),
        option('class', 'c', 'class', flag=False),
        option('worktype', 'w', 'work type (lab, cw, hw, tst)', flag=False),
        option('lastname', 'l', 'lastname of person to who helping', flag=False),
        option('year', 'y', 'year', flag=False),
        option('number', 'N', 'work number (1, 2, 3...)', flag=False),
        option('theme', 't', 'theme of work', flag=False),
        option('profile', 'p', 'a profile to use with set of pre-defined arguments', flag=False),
    )

    def handle(self):
        profile = self.option('profile')

        data = {
            'university': self.option('university'),
            'group': self.option('group'),
            'semester_number': self.option('semnumber'),
            'class': self.option('class'),
            'work_type': self.option('worktype'),
            'lastname': self.option('lastname'),
            'year': self.option('year'),
            'number': self.option('number'),
            'theme': self.option('theme'),
        }

        if profile:
            profile_data = self._load_profile(profile)
            data.update(profile_data)

        dir_name = self.build_directory_name(**data)
        self.line(dir_name)

    def build_directory_name(
        self,
        university,
        group,
        semester_number,
        class_,
        work_type,
        lastname,
        year,
        number,
        theme,
    ) -> str:
        return (
            f'u.'
            f'{university}.'
            f'{group}.'
            f'{semester_number}sem-{year}.'
            f'{class_}.'
            f'help-{lastname}-'
            f'{number}{work_type}.'
            f'{theme}'
        )

    def _load_profile(self, profile_name: str) -> dict:
        '''Load profile by name.'''
        loader = ProfileManager()
        profile = loader.load_profile(profile_name)
        return profile


