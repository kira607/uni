import json

from uni.report_creator.config import ProjectConfig
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


def main():
    
    app = UniCliApp()
    app.run('-h')


if __name__ == '__main__':
    main()
