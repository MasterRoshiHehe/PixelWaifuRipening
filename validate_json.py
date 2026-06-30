import os, json
root = r'd:\Modding\Stardew\mods\PixelWaifuRipening'

def strip_comments(text):
    out = []
    i = 0
    in_string = False
    escape = False
    in_line_comment = False
    in_block_comment = False
    while i < len(text):
        c = text[i]
        n = text[i+1] if i + 1 < len(text) else ''
        if in_line_comment:
            if c == '\n':
                in_line_comment = False
                out.append(c)
            i += 1
            continue
        if in_block_comment:
            if c == '*' and n == '/':
                in_block_comment = False
                i += 2
            else:
                if c == '\n':
                    out.append(c)
                i += 1
            continue
        if in_string:
            out.append(c)
            if escape:
                escape = False
            elif c == '\\':
                escape = True
            elif c == '"':
                in_string = False
            i += 1
            continue
        if c == '"':
            in_string = True
            out.append(c)
            i += 1
            continue
        if c == '/' and n == '/':
            in_line_comment = True
            i += 2
            continue
        if c == '/' and n == '*':
            in_block_comment = True
            i += 2
            continue
        out.append(c)
        i += 1
    return ''.join(out)

for dirpath, _, filenames in os.walk(root):
    for filename in filenames:
        if filename.endswith('.json'):
            path = os.path.join(dirpath, filename)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    text = f.read()
                stripped = strip_comments(text)
                json.loads(stripped)
            except Exception as e:
                print(path)
                if isinstance(e, json.JSONDecodeError):
                    print(f'  line {e.lineno}, col {e.colno}: {e.msg}')
                else:
                    print(f'  {type(e).__name__}: {e}')
