# かかくらべ電卓の PrivacyPolicy.md / Terms.md から privacy.html / terms.html を作る
# 使い方: python3 build.py （アプリのリポジトリが ../かかくらべ にある前提）
import html, re, pathlib, unicodedata
here = pathlib.Path(__file__).parent
app = here.parent / unicodedata.normalize("NFC", "かかくらべ") / unicodedata.normalize("NFC", "かかくらべ")
tpl = (here / "template.html").read_text(encoding="utf-8")

def build(src_name, title, out_name):
    text = re.sub(r"<!--.*?-->", "", (app / src_name).read_text(encoding="utf-8"), flags=re.S)
    body, footer, para = [], [], []
    def flush():
        if not para: return
        items = [l for l in para if l.startswith("・")]
        rest = [l for l in para if not l.startswith("・")]
        if rest: body.append("<p>" + "<br>".join(html.escape(l) for l in rest) + "</p>")
        if items: body.append("<ul>" + "".join(f"<li>{html.escape(l[1:])}</li>" for l in items) + "</ul>")
        para.clear()
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("# ") or not s: flush(); continue
        if s.startswith("## "): flush(); body.append(f"<h2>{html.escape(s[3:].strip())}</h2>"); continue
        if s.startswith(("制定日：", "改定日：")): flush(); footer.append(html.escape(s)); continue
        para.append(s)
    flush()
    out = tpl.replace("{{TITLE}}", title).replace("{{BODY}}", "\n".join(body) + f'<p class="date">{"<br>".join(footer)}</p>')
    (here / out_name).write_text(out, encoding="utf-8")
    print(f"{out_name} を更新しました")

build("PrivacyPolicy.md", "プライバシーポリシー", "privacy.html")
build("Terms.md", "利用規約", "terms.html")
