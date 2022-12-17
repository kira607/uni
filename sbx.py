import json
import shutil

from pathlib import Path

from uni.report_creator.config import ProjectConfig
from uni.report_creator.resource import ResourceCreator
from uni.cli import UniCliApp


example = '''{
    "meta": {
        "project_name": "report"
    },
    "document": {
        "group": "0335",
        "title": [
            "ЛАБОРАТОРНАЯ РАБОТА №<N>",
            "по дисциплине «<DISCIPLINE>»",
            "Тема: <THEME>"
        ],
        "partners": null,
        "teacher": "Перподов П.П.",
        "year": null,
        "chapters": {
            "task": "Задание",
            "solution": "Решение"
        },
        "new_page": true
    },
    "resources": {
        "photo": true,
        "resources": true,
        "scripts": true,
        "build_script": true
    }
}'''


def config_test():
    config = json.loads(example)
    config = ProjectConfig(**config)
    with open('tmp.json', 'w') as f:
        json.dump(config.json(indent=4, ensure_ascii=False), f, indent=4, ensure_ascii=False)


def print_tree(root, tree, fold_level=0):
    skip = '|    '
    last_folded = '└── '
    mid_folded = '├── '

    print(root)

    for i, (item, subs) in enumerate(tree.items()):
        fold_string = last_folded if i == len(tree) - 1 else mid_folded
        print_item = f'{skip*fold_level}{fold_string}{item}'

        if not subs:
            print(print_item)
            continue

        print_tree(f'{skip*fold_level}{fold_string}{item}', subs, fold_level+1)


def tree_stuff():
    tree = (
        'u.leti...', 
        {
            'modules': {
                'chapters': {
                    'chapter1.tex': None,
                    'chapter2.tex': None,
                    '...': None,
                },
                'preamble.tex': None,
                'title_page.tex': None,
            },
            'out': {
                '<project_name>.pdf': None,
                '...': None,
            },
            'photo': {'...': None},
            'resources': {'...': None},
            'scripts': {'...': None},
            'build_report.sh': None,
            '<project_name>.tex': None,
        }
    )
    print_tree(tree)


def cleanup(target: Path):
    for item in target.iterdir():
        item = Path(item)
        if item.is_dir():
            cleanup(item)
            print(f'removing {item}')
            shutil.rmtree(str(item))
        else:
            print(f'removing {item}')
            item.unlink()


def resources_sandbox():
    t_area = Path('/home/kirill/programming/uni/testing_area')
    target = Path(t_area, 'target')
    
    # cleanup(target); exit(0)

    resource_creator = ResourceCreator()

    file_resource = resource_creator.create_resource(Path(t_area, 'test.txt'))
    file_resource.deploy(target)

    template_resource = resource_creator.create_resource(Path(t_area, 'test_template.txt.template'))
    template_resource.deploy(target, data='substituted test data')

    dir_resource = resource_creator.create_resource(Path(t_area, 'complex_resource'))
    # dir_resource.add_sub_resource(FileResource(Path(t_area, 'complex_resource/test.txt')))
    # dir_resource.add_sub_resource(TemplateResource(Path(t_area, 'complex_resource/test_template.txt.template')))
    # dir_resource.add_sub_resource(IgnoredResource(Path(t_area, 'complex_resource/test.txt.ignored')))
    dir_resource.deploy(target, data='substituted test data complex', **{'task1': 'Задача №#', 'task2': 'Задача №#'})


def cli_sandbox():
    app = UniCliApp()
    app.run('-h')


def main():
    resources_sandbox()


if __name__ == '__main__':
    main()
