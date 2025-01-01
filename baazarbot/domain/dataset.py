from enum import StrEnum

from loguru import logger
try:
    from datasets import Dataset, DatasetDict, concatenate_datasets
except ImportError:
    logger.warning("Huggingface datasets not installed. Install with `pip install datasets`")

from baazarbot.domain.base import VectorBaseDocument
from baazarbot.domain.types import DataCategory


class DatasetType(StrEnum):
    INSTRUCTION = "instruction" 
    PREFERENCE = "preference"

class InstructDatasetSample(VectorBaseDocument):
    instruction: str
    answer: str

    class Config:
        category = DataCategory.INSTRUCT_DATASET_SAMPLES

class InstructDataset(VectorBaseDocument):
    category: DataCategory
    samples: list[InstructDatasetSample]
    
    class Config:
        category = DataCategory.INSTRUCT_DATASET
    
    @property
    def num_samples(self) -> int:
        return len(self.samples)
    
    def to_huggingface(self) -> Dataset:
        instructions = [sample.instruction for sample in self.samples]
        answers = [sample.answer for sample in self.samples]
        samples_dict = {
            "instructions": instructions,
            "answers": answers,
        }
        return Dataset.from_dict(samples_dict)

class TrainTestSplit(VectorBaseDocument):
    train: dict
    test: dict
    test_split_size: float
        
    def to_huggingface(self, flatten: bool = False) -> DatasetDict:
        train = {category.value: dataset.to_huggingface() for category, dataset in train.items()}
        test = {category.value: dataset.to_huggingface() for category, dataset in test.items()}
        
        if flatten:
            train = concatenate_datasets([dataset for dataset in train.values()])
            test = concatenate_datasets([dataset for dataset in test.values()])
        else:
            train = Dataset.from_dict(train)
            test = Dataset.from_dict(test)
        return DatasetDict({"train":train, "test":test})

class InstructTrainTestSplit(TrainTestSplit):
    train: dict[DataCategory, InstructDataset]
    test: dict[DataCategory, InstructDataset]
    test_split_size: float 
    
    class Config:
        category = DataCategory.INSTRUCT_DATASET

class PreferenceDataset(VectorBaseDocument):
    category: DataCategory
    samples: list[PreferenceDatasetSample]

    class Config:
        category = DataCategory.PREFERENCE_DATASET

    @property
    def num_samples(self) -> int:
        return len(self.samples)

    def to_huggingface(self) -> "Dataset":
        data = [sample.model_dump() for sample in self.samples]

        return Dataset.from_dict(
            {
                "prompt": [d["instruction"] for d in data],
                "rejected": [d["rejected"] for d in data],
                "chosen": [d["chosen"] for d in data],
            }
        )


class PreferenceTrainTestSplit(TrainTestSplit):
    train: dict[DataCategory, PreferenceDataset]
    test: dict[DataCategory, PreferenceDataset]
    test_split_size: float

    class Config:
        category = DataCategory.PREFERENCE_DATASET


def build_dataset(dataset_type, *args, **kwargs) -> InstructDataset | PreferenceDataset:
    if dataset_type == DatasetType.INSTRUCTION:
        return InstructDataset(*args, **kwargs)
    elif dataset_type == DatasetType.PREFERENCE:
        return PreferenceDataset(*args, **kwargs)
    else:
        raise ValueError(f"Invalid dataset type: {dataset_type}")
