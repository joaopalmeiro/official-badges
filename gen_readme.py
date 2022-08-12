import json
from operator import itemgetter

import mdformat
from mdutils.mdutils import MdUtils
from natsort import natsorted, ns
from sortedcontainers import SortedSet

INPUT_FILENAME: str = "badges.json"
OUTPUT_FILENAME: str = "README"

# https://github.com/Nicceboy/python-markdown-generator
# https://github.com/didix21/mdutils
# https://github.com/Ileriayo/markdown-badges
# https://github.com/aleen42/badges
if __name__ == "__main__":
    with open(INPUT_FILENAME, "r") as f:
        badges = json.load(f)
        # print(badges)

        # https://stackoverflow.com/a/73050
        # https://natsort.readthedocs.io/en/master/examples.html#locale-aware-sorting-human-sorting
        # https://natsort.readthedocs.io/en/master/examples.html#case-sort
        # badges = humansorted(badges, key=itemgetter("project"))
        badges = natsorted(badges, alg=ns.IGNORECASE, key=itemgetter("project"))
        # print(badges)

    # https://stackoverflow.com/a/45456099
    # https://pypi.org/project/sortedcontainers/
    # https://grantjenks.com/docs/sortedcontainers/sortedset.html
    languages = SortedSet({badge["language"] for badge in badges})
    # print(languages)

    mdFile = MdUtils(file_name=OUTPUT_FILENAME)

    mdFile.new_header(level=1, title="official-badges")
    mdFile.new_paragraph(
        'List of "official" badges shared by the respective projects to add to README files.'
    )

    mdFile.new_header(level=2, title="Badges")

    badge_table_cols = ["Project", "Badge", "Markdown"]
    n_cols = len(badge_table_cols)

    badge_tables = {language: badge_table_cols.copy() for language in languages}

    for badge in badges:
        project = f'[{badge["project"]}]({badge["source"]})'
        md = f'`{badge["badge"]}`'

        badge_tables[badge["language"]].extend([project, badge["badge"], md])

    for language, badge_table in badge_tables.items():
        mdFile.new_header(level=3, title=language)

        n_rows = len(badge_table) // n_cols
        mdFile.new_table(
            columns=n_cols, rows=n_rows, text=badge_table, text_align="left"
        )

    mdFile.create_md_file()

    # https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html#format-a-file
    # https://github.com/executablebooks/mdformat-tables
    # https://github.com/executablebooks/mdformat/issues/283
    mdformat.file(f"{OUTPUT_FILENAME}.md", extensions={"tables"})
