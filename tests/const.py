TIMEWARRIOR_STDIN = r"""kaiten.issue_pattern: \d{6,7}$
kaiten.token: MYKAITEN_TOKEN
kaiten.url: https://kaiten.mysite.ru


[
{"id":32,"start":"20240715T075500Z","end":"20240715T081728Z","tags":["DEV","KTN-1733551"], "annotation":"sometext"},
{"id":31,"start":"20240715T100059Z","end":"20240715T114820Z","tags":["KTN-1733551"],"annotation":"sometext"},
{"id":30,"start":"20240715T120059Z","end":"20240715T124820Z","tags":["DEV","KTN-1733551"]},
{"id":29,"start":"20240715T100059Z","end":"20240715T114820Z","tags":["SOMETAG", "DEV"], "annotation":"another task"}
]
"""
TIMEWARRIOR_MULTIPLE_TAGS_STDIN = r"""kaiten.issue_pattern: \d{6,7}$
kaiten.token: MYKAITEN_TOKEN
kaiten.url: https://kaiten.mysite.ru


[
{"id":32,"start":"20240715T075500Z","end":"20240715T081728Z","tags":["DEV","KTN-1733551", "KTN-1733552"], "annotation":"sometext"},
{"id":30,"start":"20240715T100059Z","end":"20240715T114820Z","tags":["DEV","KTN-1733551"],"annotation":"sometext"}
]
"""
TIMEWARRIOR_MULTIPLE_TYPES_STDIN = r"""kaiten.issue_pattern: \d{6,7}$
kaiten.token: MYKAITEN_TOKEN
kaiten.url: https://kaiten.mysite.ru


[
{"id":32,"start":"20240715T075500Z","end":"20240715T081728Z","tags":["DEV","KTN-1733551"], "annotation":"sometext"},
{"id":30,"start":"20240715T100059Z","end":"20240715T114820Z","tags":["DEV", "DEV", "KTN-1733551"],"annotation":"sometext"}
]
"""
TIMEWARRIOR_NOT_FOUND_STDIN = r"""kaiten.issue_pattern: \d{6,7}$
kaiten.token: MYKAITEN_TOKEN
kaiten.url: https://kaiten.mysite.ru


[
{"id":32,"start":"20240715T075500Z","end":"20240715T081728Z","tags":["DEV","KTN-1733552"], "annotation":"sometext"},
{"id":30,"start":"20240715T100059Z","end":"20240715T114820Z","tags":["DEV", "KTN-1733552"],"annotation":"sometext"}
]
"""
