uni
===

A python CLI tool to create latex projects from templates

## Installation

### Prerequisites

`python >= 3.7`

### Installation

```sh
pip install -e path/to/uni/root
```

## Usage

Project structure goes as follows:

```
u.leti...
├── modules
|    ├── chapters
|    |    ├── chapter1.tex
|    |    ├── chapter2.tex
|    |    └── ...
|    ├── preamble.tex
|    └── title_page.tex
├── out
|    ├── <project_name>.pdf
|    └── ...
├── photo
|    └── ...
├── resources
|    └── ...
├── scripts
|    └── ...
├── build_report.sh
└── <project_name>.tex
```

First, create a project directory with
command `mkdir`.

```bash
$ uni mkdir
```

Then cd to newly created folder
Here create a config with `init` command.

```bash
$ uni init
```

Adjust created configuration and run `deploy` command.

```bash
$ uni deploy
```

## Commands

### touch

```sh
$> uni report <project_name>
```

University repos naming:

- u.
- universety name (leti)
- group (9892, 0335)
- semester-year (sem-2022)
- class name (algo-and-ds, communications, etc.)
- work signature:
  - [help] - optional help tag
  - work type (lab, hw, cw)
  - [lastname] - optional lastname of person I helped
- [work theme].

Examples:

- u.leti.9892.6sem-2022.algo-and-ds.1lab.rbtree
- u.leti.0335.5sem-2022.engineering-drawing.cw
- u.leti.9892.6sem-2022.algo-and-ds.help-1lab-evseeva.flow-network

#### Args:

- _project_name_: The name of the project.
This name will be applied to the main file in
the project.

#### Options:


### create

create report template at where you are right now.
