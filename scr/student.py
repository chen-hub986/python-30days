from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Student:
    name: str
    scores: List[float] = field(default_factory=list)

    def average_score(self) -> float:
        if not self.scores:
            return 0
        return sum(self.scores) / len(self.scores)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "scores": self.scores
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Student':
        return cls(name=data['name'], scores=data['scores'])
