import os
import uuid
from dataclasses import dataclass
from typing import List, Optional

import commands.config as cfg


@dataclass(frozen=True)
class Image:
    name: str
    version: str
    size: int
    cmd: List[str]
    dir: str
    working_dir: Optional[str]

    @property
    def content_dir(self):
        return os.path.join(self.dir, 'contents')


@dataclass(frozen=True)
class Container:
    id: str
    root_dir: str
    rw_dir: str
    work_dir: str

    @staticmethod
    def init_from_image(image: Image):
        id = f'{image.name.replace("/", "-")}_{image.version}_{uuid.uuid4()}'
        root_dir = os.path.join(cfg.CONTAINER_DATA_DIR, id)

        rw_dir = os.path.join(root_dir, 'rw')
        work_dir = os.path.join(root_dir, 'work')

        for d in (root_dir, rw_dir, work_dir):
            if not os.path.exists(d):
                os.makedirs(d)

        return Container(id, root_dir, rw_dir, work_dir)
