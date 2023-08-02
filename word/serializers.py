from word.models import *

def serializeWord(entity: Word) -> dict:
    return{
        "id": entity.pk,
        "title": entity.title,
        "author": entity.author,
        "age": entity.age,
        "content": entity.content,
        "create_at": entity.created_at,
        "likes": entity.likes,
        "view": entity.views,
    }