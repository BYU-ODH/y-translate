from pydantic import BaseModel


class TranslationRequest(BaseModel):
    words: str