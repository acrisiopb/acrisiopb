import requests
import re
import xml.etree.ElementTree as ET

USERNAME = "acrisio-cruz"
README_FILE = "README.md"
SECTION_TITLE = "## 🏆 Certificações e Distintivos"

url = f"https://www.credly.com/users/acrisio-cruz/badges#credly"

response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
if response.status_code != 200:
    print(f"❌ Erro ao acessar o feed RSS da Credly: {response.status_code}")
    exit(1)

root = ET.fromstring(response.content)

badges = []
for item in root.findall(".//item"):
    title = item.find("title").text
    link = item.find("link").text
    image_match = re.search(r'src="(https:[^"]+)"', item.find("description").text or "")
    image_url = image_match.group(1) if image_match else None
    if image_url:
        badges.append((title, link, image_url))

if not badges:
    print("⚠️ Nenhum distintivo encontrado. Verifique se o perfil é público.")
    exit(0)

badges_md = f"{SECTION_TITLE}\n\n<div align='center'>\n\n"
for title, link, image_url in badges:
    badges_md += f"[![{title}]({image_url})]({link})\n"
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

print(f"✅ Distintivos atualizados com sucesso! ({len(badges)} encontrados)")
