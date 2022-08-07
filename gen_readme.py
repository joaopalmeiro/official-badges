import json

import mdformat
from mdutils.mdutils import MdUtils

FILENAME = "README"

# https://github.com/Nicceboy/python-markdown-generator
# https://github.com/didix21/mdutils
# https://github.com/Ileriayo/markdown-badges
if __name__ == "__main__":
    with open("badges.json", "r") as f:
        badges = json.load(f)
        # print(badges)

    mdFile = MdUtils(file_name=FILENAME)

    mdFile.new_header(level=1, title="official-badges")
    mdFile.new_paragraph(
        'List of "official" badges shared by the respective projects to add to README files.'
    )

    mdFile.new_header(level=2, title="Badges")

    badge_table = ["Project", "Badge", "Markdown"]
    n_cols = len(badge_table)
    n_rows = len(badges) + 1

    for badge in badges:
        project = f'[{badge["project"]}]({badge["source"]})'
        md = f'`{badge["badge"]}`'

        badge_table.extend([project, badge["badge"], md])

    mdFile.new_table(columns=n_cols, rows=n_rows, text=badge_table, text_align="left")

    mdFile.create_md_file()

    # https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html#format-a-file
    # https://github.com/executablebooks/mdformat-tables
    # https://github.com/executablebooks/mdformat/issues/283
    mdformat.file(f"{FILENAME}.md", extensions={"tables"})