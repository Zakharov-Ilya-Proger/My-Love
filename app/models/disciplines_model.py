from typing import Dict, List
from pydantic import BaseModel


class Disciplines(BaseModel):
    lessons_and_related_groups: Dict[str, List[str]]
