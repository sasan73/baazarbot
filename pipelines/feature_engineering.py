from zenml import pipeline

from steps import feature_engineering as fe_steps

@pipeline
def feature_engineering() -> list[str]:
    raw_documents = fe_steps.get_data_warehouse()
    cleaned_documents = fe_steps.clean_documents(raw_documents)
    cleaning_step = fe_steps.load_to_vector_db(cleaned_documents)

    embedded_documents = fe_steps.chunk_and_embed(cleaned_documents)
    embedding_step = fe_steps.load_to_vector_db(embedded_documents)
    return [cleaning_step.invocation_id, embedded_documents.invocation_id]
