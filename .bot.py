#!/bin/python3

import sys

files_to_botify = sys.argv[1:]
for filename in files_to_botify:
    backup_filename = f"{filename}.botbackup"
    with open(filename) as file:
        lines = file.readlines()
    with open(backup_filename, "w+") as backup_file:
        backup_file.writelines(lines)
    for (index, line) in enumerate(lines):
        if line.startswith("(BOT):"):
            origin_filename = line.lstrip("(BOT):").strip()
            with open(origin_filename) as origin_file:
                contents_to_insert = origin_file.read()
            if origin_filename.find(".py") > -1:
                filetype = "python"
            elif origin_filename.find(".") > -1:
                filetype = origin_filename.split(".")[-1]
            else:
                filetype = ""
            lines[index] = f"```{filetype}\n{contents_to_insert}```\n"

    if filename.__contains__(".botify"):
        filename = filename.rstrip(".botify")
    with open(filename, "w+") as file:
        file.writelines(lines)
