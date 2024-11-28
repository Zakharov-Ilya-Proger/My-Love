from typing import Dict, List
from pydantic import BaseModel, RootModel


class Disciplines(RootModel):
    root: Dict[str, List[str]]
