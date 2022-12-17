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
project_folder
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

### University repos naming:

- u.
- universety name (leti)
- group (9892, 0335)
- semester-year (\<N>sem-\<YYYY>)
- class name (algo-and-ds, communications, etc.)
- work signature:
  - [help]-[lastname] - optional help tag and lastname of person I helped
  - [N] work type (lab, hw, cw)
- [work theme].

Examples:

- u.leti.9892.6sem-2022.algo-and-ds.1lab.rbtree
- u.leti.0335.5sem-2022.engineering-drawing.cw
- u.leti.9892.6sem-2022.algo-and-ds.help-evseeva-1lab.flow-network

### Configuring profile

`uni/src/.data/profiles.yaml`

```yaml
default:
  universety: leti
  group: 0335
  semester: 5
  year: 2022
  classes:
    5:
      - algo-and-ds
      - ...
    6: 
      - ...
old:
  universety: leti
  group: 9892
  semester: auto
  year: auto
  classes:
    5:
      - algo-and-ds
      - ...
    6: 
      - ...
```

### Common case

First, create a project directory with
[`mkdir` command](#mkdir) and `cd` to it.

```bash
$ uni mkdir
```

Here create a config with [`init` command](#init).

```bash
$ uni init
```

Adjust created configuration and run 
[`deploy` command](#deploy).

```bash
$ uni deploy
```

## Commands

### mkdir

Create a project directory.

```sh
$> uni mkdir <universety> <group> <semester-number> <class> <work-type> [lastname] [year] [work-number] [theme] [profile]
```

#### Args:

#### Options:

- `-u, --universety` - universety of studying.
- `-g, --group` - studying group.
- `-s, --semester-number` - semester number
- `-c, --class` - class
- `-w, --work-type` - work type (lab, cw, hw, tst)
- `-l, --lastname=LASTNAME` - lastname of person to who helping
- `-y, --year=YEAR` - year
- `-n, --number=NUMBER` - work number (1, 2, 3...)
- `-t, --theme=THEME` - theme of work
- `-p, --profile=PROFILE` - a profile to use with set of pre-defined arguments.

### init

Create a configuration file from template.

```bash
$ uni init [template]
```

#### Args:

- _project_name_: The name of the project.
This name will be applied to the main file in
the project.

#### Options:

### deploy

#### Args:

- _project_name_: The name of the project.
This name will be applied to the main file in
the project.

#### Options:

