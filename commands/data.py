import os
from dataclasses import dataclass
from typing import List, Optional


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
