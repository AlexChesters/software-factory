from typing import NamedTuple

from typesafe_sdk import Choice, TypeSafeClient

DEFAULT_EFFORT = "medium"

COMPLEXITIES = {
    "low": "A well-defined, small/trivial change to existing behaviour.",
    "moderate": "Typical day-to-day software engineering tasks backed with a clear plan.",
    "high": "Very large and complex changes across many aspects of the codebase."
}


class ModelChoice(NamedTuple):
    model_name: str
    effort: str


def get_model_choice(*, task: str) -> ModelChoice:
    model = "claude-sonnet-5-5"

    with TypeSafeClient() as client:
        response = client.system_one(
            state={"task": task},
            questions={
                "complexity": Choice(
                    instructions="How complex is the given software engineering task?",
                    criteria=COMPLEXITIES
                )
            }
        )

        complexity_choice = response.answers["complexity"].choice

    if complexity_choice == "low":
        model = "claude-haiku-5-5"
    elif complexity_choice == "moderate":
        model = "claude-sonnet-5-5"
    elif complexity_choice == "high":
        model = "claude-opus-5-5"

    return ModelChoice(model_name=model, effort=DEFAULT_EFFORT)
