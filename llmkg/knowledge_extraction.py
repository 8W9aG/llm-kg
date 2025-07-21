"""A representation of a triplet."""

from pydantic import BaseModel

from .triplet import Triplet


class KnowledgeExtractionModel(BaseModel):
    """The model for extracting a list of triplets from an instructor pipeline."""

    entities: list[Triplet]
