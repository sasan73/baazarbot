from sklearn.model_selection import train_test_split

from baazarbot.domain.dataset import TrainTestSplit

def split_dataset_samples(dataset: InstructDataset | PreferenceDataset, test_size: float) -> TrainTestSplit:
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
