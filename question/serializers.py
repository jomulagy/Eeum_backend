from question.models import *


def serializeQuestion(entity: Question) -> dict:
    return {
        "author":entity.author,
        "title": entity.title,
        "content": entity.content,
        "views": entity.views,
    }

def serializeComment(entity: Comment) -> dict:
    return {
        "Comment_id": entity.id,
        "author": entity.author,
        "content": entity.content,
        "created_at": entity.created_at,
    }

def serializeMessage(entity: Message) -> dict:
    
    status = "unread"

    if entity.read == False:
        status = "unread"
    else:
        status = "read"

    return {
        "uset": entity.user,
        "content": entity.content,
        "status": status,
    }
