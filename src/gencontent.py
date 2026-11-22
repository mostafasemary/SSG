import os
from pathlib import Path

from block_markdown import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            stripped = line[2:].strip()
            return stripped
    raise Exception("Title not found")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        md_content = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    html = markdown_to_html_node(md_content).to_html()
    page_title = extract_title(md_content)

    template_temp_1 = template_content.replace("{{ Title }}", page_title)
    template_temp_2 = template_temp_1.replace("{{ Content }}", html)
    template_temp_3 = template_temp_2.replace('href="/', f'href="{basepath}')
    final_template = template_temp_3.replace('src="/', f'src="{basepath}')

    dest_folder = os.path.dirname(dest_path)
    if dest_folder != "":
        os.makedirs(dest_folder, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            if filename.endswith(".md"):
                dest_path = Path(dest_path).with_suffix(".html")
                generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
