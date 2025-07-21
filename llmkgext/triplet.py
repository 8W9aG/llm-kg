"""A representation of a triplet."""

from pydantic import BaseModel


class Triplet(BaseModel):
    """The triplet definition for the instructor pipeline."""

    subject: str
    predicate: str
    object: str
