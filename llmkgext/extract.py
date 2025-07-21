"""A function for extracting triplets from some text."""

# pylint: disable=broad-exception-caught
import datetime
import logging

import instructor
import nltk  # type: ignore
from groq import Groq
from nltk.tokenize import sent_tokenize  # type: ignore
from textblob import TextBlob  # type: ignore
from timefhuman import tfhConfig, timefhuman  # type: ignore

from .knowledge_extraction import KnowledgeExtractionModel
from .triplet import Triplet

nltk.download("punkt_tab")


SYSTEM_PROMPT_KG = """
Some text will be provided to you. Extract all the entities and their relationships to each other to build a knowledge graph and output it in JSON format. Make sure you get every relationship, there is usually more than one.

EXAMPLE INPUT:
Rodrigo Martins Vaz, known as Rodrigo (born 24 May 1971), is a retired Brazilian footballer.

EXAMPLE JSON OUTPUT:
{
  "entities: [
    {
      "subject": "Rodrigo Martins Vaz",
      "predicate": "is",
      "object": "retired"
    },
    {
      "subject": "Rodrigo Martins Vaz",
      "predicate": "is",
      "object": "Brazilian"
    },
    {
      "subject": "Rodrigo Martins Vaz",
      "predicate": "is",
      "object": "footballer"
    },
    {
      "subject": "Rodrigo Martins Vaz",
      "predicate": "born",
      "object": "24 May 1971"
    }
  ]
}
"""


def _is_objective(triplet: Triplet) -> bool:
    sentence = " ".join(
        [
            triplet.subject,
            triplet.predicate,
            triplet.object,
        ]
    )
    sentence_blob = TextBlob(sentence)
    return sentence_blob.sentiment.subjectivity < 0.5  # type: ignore


def extract(
    text: str, publish_date: datetime.datetime | None = None, model: str | None = None
) -> list[Triplet]:
    """Extract triplets from text."""
    if publish_date is None:
        publish_date = datetime.datetime.now()
    if model is None:
        model = "deepseek-r1-distill-llama-70b"

    # Normalise sentence
    config = tfhConfig(return_matched_text=True, now=publish_date)
    sentences = []
    for sentence in sent_tokenize(text):
        try:
            dates = timefhuman(sentence, config=config)
            if not isinstance(dates, list):
                raise ValueError("dates is not a list.")
            dates.reverse()
            for date in dates:
                _, replacement_pos, dt = date
                start_idx, end_idx = replacement_pos
                sentence = sentence[:start_idx] + dt.isoformat() + sentence[end_idx:]
        except Exception as exc:
            logging.warning(str(exc))
        sentences.append(sentence)

    # Extract Knowledge
    try:
        client = instructor.from_groq(Groq(), mode=instructor.Mode.JSON)
        response = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            response_model=KnowledgeExtractionModel,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT_KG,
                },
                {
                    "role": "user",
                    "content": ". ".join(sentences),
                },
            ],
        )
        return [x for x in response.entities if _is_objective(x)]
    except Exception as exc:
        logging.warning(str(exc))
        return []
