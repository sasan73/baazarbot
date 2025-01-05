from sklearn.model_selection import train_test_split

from baazarbot.domain.dataset import DatasetType, TrainTestSplit, InstructTrainTestSplit, build_dataset

def split_dataset_samples(datasets: dict, test_size: float, dataset_type: DatasetType) -> TrainTestSplit:
    category_train = {}
    category_test = {}

    for category, category_dataset in datasets.items():

        train_samples, test_samples = train_test_split(category_dataset.samples, test_size=test_size, shuffle=True)

        trainset = build_dataset(dataset_type=dataset_type, samples=train_samples, category=category)
        testset = build_dataset(dataset_type=dataset_type, samples=test_samples, category=category)

        category_train[category] = trainset
        category_test[category] = testset

    return InstructTrainTestSplit(
        train = category_train,
        test = category_test,
        test_split_size = test_size,
    )
