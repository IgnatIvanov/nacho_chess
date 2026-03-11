from pydantic import BaseModel


class SendMsgTask(BaseModel):
    chat_id: int
    text: str
    reply_to_msg_id: int|None
