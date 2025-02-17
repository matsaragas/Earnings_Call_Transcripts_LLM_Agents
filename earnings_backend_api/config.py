class Settings:

    VECTOR_DIR: str = 'vectorize'
    SYSTEM_TEMPLATE: str = """
    Answer the user's questions based on the below context. 
    If the context doesn't contain any relevant information to the questions, don't make someting up
    and just reply information cannot be fount:
    <context>
    {context}
    </context>
    """
    MODEL_NAME: str = "gpt-4o"
    EMBEDDING_NAME: str = "text-embedding-ada-002"