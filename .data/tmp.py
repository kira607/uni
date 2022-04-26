data = f'''
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
                      & \\begin{{tabular}}{{p{{60mm}}}} \\\\ \\hline \\end{{tabular}} &  \\\\\\\\        
    Преподаватель     & \\begin{{tabular}}{{p{{60mm}}}} \\\\ \\hline \\end{{tabular}} & \\teachername \\\\\\\\
\\end{{tabular}}

\\begin{{center}}
    Санкт-Петербург\\\\
    \\labyear
\\end{{center}}

\\newpage'''

import os
with open(os.path.abspath('.data/files_templates/title_page'), 'w+') as f:
    f.write(data)