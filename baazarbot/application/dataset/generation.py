from ABC import abc, abstractmethod

from transformers import AutoTokenizer, AutoModelForCaulsalLM
from langchain_core.exceptions import OutputParserException
from langchain_core.language_models.fake import FakeListLLM
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from loguru import logger


from baazarbot import domain
from baazarbot.domain.dataset import DatasetType, TrainTestSplit, InstructDatasetSample, PreferenceDatasetSample
from baazarbot.domain.prompt import GenerateDatasetSamplesPrompt, Prompt
from baazarbot.domain.cleaned_documents import CleanedDocument
from baazarbot.domain.type import DataCategory
from baazarbot.domain import utils
from baazarbot.settings import settings

class DatasetGeneator(ABC):
    tokenizer = AutoTokenizer.from_pretrained(settings.DATASET_GENERATION_MODEL_ID)
    dataset_type: DatasetType | None=None

    system_prompt_template = """You are a helpful assistnat who generate Persian {dataset_format} based on the given context. \
        Provide your response in JSON format."""
    
    prompt_template_str: str | None = None

    @classmethod
    def get_system_prompt(cls) -> Prompt:
        assert cls.dataset_type is not None, "Dataset type must be set before calling get_system_prompt()"

        dataset_format = "instruction-answer pairs" if cls.dataset_type == DatasetType.INSTRUCTION else "instruction-answer triples"
        
        input_variables = {
            "dataset_format": dataset_format
        }
        
        content = system_prompt.format(**input_variables)
        return Prompt(
            template=cls.system_prompt_template,
            input_variables=input_variables,
            content=content,
        )
    
    @classmethod 
    def get_prompts(cls, documents: list[CleanedDocument]) -> dict[DataCategory, list[GenerateDatasetSamplesPrompt]]
        grouped_prompts = {}
        grouped_docs = documetns.group_by_category()
        for category, category_docs in grouped_docs.items():
            prompts[category] = [cls.get_prompt(doc) for doc in category_docs]
        return grouped_prompts

    @classmethod
    def get_prompt(cls, document: CleanedDocument) -> GenerateDatasetSamplesPrompt:
        
        data_category = document.get_category()
        
        prompt_template = PromptTemplate.from_template(
            template=cls.prompt_template_str,
            template_format="jinja2",
        )
        input_variables = {
            "extract": document.content,
        }
        prompt = prompt_template.format(**input_variables)
        prompt_tokens = cls.tokenizer.encode(prompt)
        if len(prompt_tokens) > cls.tokenizer.model_max_length:
            prompt_tokens = prompt_tokens[: cls.tokenizer.model_max_length]
            prompt = cls.tokenizer.decode(prompt_tokens)

        prompt = GenerateDatasetSamplesPrompt(
            template=prompt_template.template,
            input_variables=input_variables,
            content=prompt,
            num_tokens=len(prompt_tokens),
            data_category=data_category,
            document=document,
        )
        return prompt

    @classmethod
    def generate(
        cls,
        prompts: dict[DataCategory, list[GenerateDatasetSamplesPrompt]],
        test_size: float = 0.2,
        mock: bool = False,
    ) -> TrainTestSplit:
        assert cls.dataset_type is not None, "Dataset type must be set before calling generate()"

        llm = cls._load_model(mock)
        parser = ListPydanticOutputParser(pydantic_object=cls._get_dataset_sample_type())
        chain = llm | parser

        datasets = {}
        for category, category_sample_prompts in prompts.items():
            messages = [cls._to_langchain(prompt) for prompt in category_sample_prompts]
            
            flattened_category_dataset = []
            for grouped_prompts in utils.misc.batch(category_sample_prompts, size=10):
                dataset_samples = chain.batch(grouped_prompts)

                for dataset_sample in dataset_samples:
                    flattened_category_dataset.extend(dataset_objects)

            dataset = domain.dataset.build_dataset(
                dataset_type=cls.dataset_type,
                samples=flattened_category_dataset,
                category=category
            )

            datasets[category] = dataset

        logger.info(f"Generated {len(dataset.samples)} samples for category '{category}'.")
        processed_dataset = cls.post_process_datasets(datasets, test_size=test_size)

        return processed_dataset


    @staticmethod
    def _load_model(mock: bool = False) -> "Model":
        if mock:
            return FakeListLLM(responses=[constants.get_mocked_response(cls.dataset_type)])
        hf_model_parameters = {
            device_map="auto",
            load_in_4bit=True,
        }
        return HuggingFaceEndpoint(
            repo_id=settings.DATASET_GENERATION_MODEL_ID,
            task="text_generation",
            max_new_tokens=2000,
            do_sample=False,
            model_kwargs=hf_model_parameters,
        )


    @staticmethod
    def _to_langchain(
            prompt: GenerateDatasetSamplesPrompt,
        ) -> list[BaseMessage]:
            messages = [
                SystemMessage(content=cls.get_system_prompt().content),
                UserMessage(content=prompt.content)
            ]

            return messages

    @classmethod
    def _get_dataset_sample_type(
        cls,
    ) -> (type[InstructDatasetSample] | type[PreferenceDatasetSample]):
        return (
            InstructDatasetSample if dataset_type == DatasetType.INSTRUCTION 
            else PreferenceDatasetSample
        )

    @classmethod
    @abstractmethod
    def post_process_datasets(cls, datasets: dict, test_size: float) -> TrainTestSplit:
        pass


class InstructionDatasetGeneration(DatasetGenerator):
    dataset_type = DatasetType.INSTRUCTION
    
    prompt_template_str = """Based on the following extract, generate five instruction-answer pairs in Persian(Farsi). Each instruction \
must ask to write about a specific topic contained in the context. Each answer \
must provide a relevant paragraph based on the information found in the \
context. Only use concepts from the context to generate the instructions. \
Instructions must never explicitly mention a context, a system, a course, or an extract. \
Instructions must be self-contained and general. \
Answers must imitate the writing style of the context. \

Structure the answer in JSON format, ready to be loaded in Python by json.loads(), as a list of objects.
Do not add any extra characters and provide your response in JSON format with the following structure:
[
    {"instruction": "...", "answer": "..."},
    ...
]

Extract:
{extract}
    """

        @classmethod
        def post_process_datasets(cls, datasets: dict, test_size: float) -> InstructTrainTestSplit:
            
            category_train = {}
            category_test = {}

            for category, category_dataset in datasets.items():
                
                train_samples, test_samples = train_test_split(category_dataset.samples, test_size=test_size, shuffle=True)
                
                trainset = build_dataset(dataset_type=cls.dataset_type, samples=train_samples, data_category=category)
                testset = build_dataset(dataset_type=cls.dataset_type, samples=test_samples, data_category=category)

                category_train[category] = trainset
                category_test[category] = testset

            return InstructTrainTestSplit(
                train = category_train,
                test = category_test,
                test_size = test_size,
            )


def get_dataset_generator(dataset_type: DatasetType) -> type[DatasetGenerator]:
    if dataset_type == DatasetType.INSTRUCTION:
        return InstructionDatasetGenerator
    else:
        raise ValueError(f"Invalid dataset type: {dataset_type}")
