import json
import os
from typing import List

import commands.config as cfg
import commands.data as data


def find_images() -> List[data.Image]:
    images = []

    if not os.path.exists(cfg.IMAGE_DIR):
        return []

    for image_dir_name in os.listdir(cfg.IMAGE_DIR):
        image_dir = os.path.join(cfg.IMAGE_DIR, image_dir_name)
        with open(os.path.join(image_dir, 'manifest.json'), 'r') as manifest_file:
            manifest = json.loads(manifest_file.read())

        layers_path = os.path.join(image_dir, 'layers')

        size = sum(
            os.path.getsize(os.path.join(layers_path, layer))
            for layer in os.listdir(layers_path) if os.path.isfile(os.path.join(layers_path, layer))
        )

        # デフォルトのコマンドを取得する
        state = json.loads(manifest['history'][0]['v1Compatibility'])
        cmd = state['config']['Cmd']

        # working dirを取得する
        working_dir = state['config']['WorkingDir']
        working_dir = working_dir if working_dir else None

        image = data.Image(manifest['name'], manifest['tag'], size, cmd, image_dir, working_dir)
        images.append(image)

    return images
