from typing_extensions import Annotated
from zenml import step, get_step_context

from baazarbot.application.dataset.generation import get_dataset_generator
from baazarbot.domain.dataset import DatasetType
from baazarbot.domain.cleaned_documents import CleanedDocument
from baazarbot.domain.prompt import GenerateDatasetSamplesPrompt
from baazarbot.domain.types import DataCategory

@step
def create_prompts(
    documents: Annotated[list[CleanedDocument], "cleaned_documetns"],
    dataset_type: Annotated[DatasetType, "dataset_type"],
) -> dict[DataCategory, list[GenerateDatasetSamplesPrompt]]:
    generator = get_dataset_generator(dataset_type)
    prompts = generator.get_prompts(documents)

    step_context = get_step_context()
    step_context.add_output_metadata(output_name="prompts", metadata=get_prompt_metadata(prompts))

    return prompts

def get_prompt_metadata(category_prompts: dict) -> dict:
    metadata = {}
    token_lengths = []
    for category, prompts in category_prompts.items():
        if category not in metadata:
            metadata[category] = {}
        metadata[category]["number_of_prompts"] = len(prompts)
        token_lengths.append(prompts.num_tokens)
    metadata[category]["average_prompt_token_length"] = sum(token_lengths) / len(token_lengths)

    return metadata
