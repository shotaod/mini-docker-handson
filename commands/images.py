from terminaltables import AsciiTable

import commands.local as local
import commands.format as fmt


def exec_images():
    print('images command called!')
    return

    print('fetching images')
    images = local.find_images()
    header = [['name', 'version', 'size', 'path']]
    rows = header + [[img.name, img.version, fmt.sizeof_fmt(img.size), img.dir] for img in images]
    print(AsciiTable(rows).table)
