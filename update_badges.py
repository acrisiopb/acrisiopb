import requests
import re

USERNAME = "acrisio-cruz"
README_FILE = "README.md"
SECTION_TITLE = "## 🏆 Certificações e Distintivos"

url = f"https://www.credly.com/users/acrisio-cruz/badges"
response = requests.get(url)
if response.status_code != 200:
    print("❌ Erro ao acessar a API da Credly.")
    exit(1)

data = response.json()
badges_md = f"{SECTION_TITLE}\n\n<div align='center'>\n\n"

for badge in data.get("data", []):
    image_url = badge["badge_template"]["image_url"]
    name = badge["badge_template"]["name"]
    link = f"https://www.credly.com/badges/{badge['id']}"
    badges_md += f"[![{name}]({image_url})]({link})\n"

badges_md += "\n</div>\n"

with open(README_FILE, "r", encoding="utf-8") as f:
    content = f.read()

pattern = re.compile(rf"{SECTION_TITLE}[\s\S]*?(?=\Z)", re.MULTILINE)
if pattern.search(content):
    content = re.sub(pattern, badges_md, content)
else:
    content += "\n\n" + badges_md

with open(README_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Distintivos da Credly atualizados com sucesso!")
