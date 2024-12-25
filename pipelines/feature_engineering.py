from zenml import pipeline

from steps import feature_engineering

@pipeline
def feature_engineering() -> List[str]:
    raw_documents = feature_engineering.get_data_warehouse()
    cleaned_documents = feature_engineering.clean_documents(raw_documents)
    cleaning_step = feature_engineering.load_to_vectore_db(cleaned_documents)

    embedded_documents = feature_engineering.chunk_and_embed(cleaned_documents)
    embedding_step = feature_engineering.load_to_vectore_db(embedded_documents)
    return [cleaning_step.invocaiton_id, embedded_documents.invocaiton_id]
