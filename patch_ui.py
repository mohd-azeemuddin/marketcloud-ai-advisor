import base64, re, sys
from pathlib import Path

p = Path("frontend/index.html")
logo_file = Path("frontend/logo.png")
if not p.exists() or not logo_file.exists():
    sys.exit("Missing frontend/index.html or frontend/logo.png. Run this from the project folder.")
html = p.read_text(encoding="utf-8")
if 'class="right"' in html:
    sys.exit("Already patched. Nothing to do.")
logo = base64.b64encode(logo_file.read_bytes()).decode()

def sub(pattern, repl, flags=0):
    global html
    html, n = re.subn(pattern, lambda m: repl, html, count=1, flags=flags)
    if n != 1:
        sys.exit("Could not find: " + pattern[:50])

# 1. remove the old tab row from the main area
sub(r'\n\s*<div class="tabs">.*?</div>', '', re.S)
# 2. header: tabs on the right, then the logo image
sub(r'<span class="logo">MARKETCLOUD</span></div>',
    '<div class="right"><div class="tabs"><button class="on" data-v="chatv">Assistant</button>'
    '<button data-v="crm">CRM &amp; Audit</button><button data-v="evals">Evaluation</button></div>'
    '<img class="logo" alt="Market Cloud" src="data:image/png;base64,' + logo + '"></div></div>')
# 3. styles
sub(r'\.logo\{[^}]*\}', '.logo{height:52px;width:auto}\n.right{display:flex;align-items:center;gap:24px}')
sub(r'\.tabs\{[^}]*\}', '.tabs{display:flex;gap:4px}')
sub(r'\.tabs button\{[^}]*\}', '.tabs button{background:none;border:0;padding:8px 14px;cursor:pointer;font:inherit;font-weight:600;color:#a9b6d3;border-radius:8px}')
sub(r'\.tabs button\.on\{[^}]*\}', '.tabs button.on{color:#fff;background:#2a3556}')
sub(r'</style>', '.top{flex-wrap:wrap;gap:12px}\n</style>')

p.write_text(html, encoding="utf-8")
print("Done. Logo and header updated.")
