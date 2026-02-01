from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Uncertainty:
    """Captures what a Bear doesn't know or is unsure about."""

    missing_information: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    verification_needed: bool = False
    confidence: Optional[float] = None  # 0.0 to 1.0, None if unknown

    def add_missing(self, info: str) -> None:
        if info not in self.missing_information:
            self.missing_information.append(info)

    def add_assumption(self, assumption: str) -> None:
        if assumption not in self.assumptions:
            self.assumptions.append(assumption)

    def to_dict(self) -> dict:
        return {
            "missing_information": list(self.missing_information),
            "assumptions": list(self.assumptions),
            "verification_needed": self.verification_needed,
            "confidence": self.confidence,
        }

    def __bool__(self) -> bool:
        """True if there is any uncertainty recorded."""
        return bool(
            self.missing_information
            or self.assumptions
            or self.verification_needed
            or self.confidence is not None
        )
