from misc import dp
from messages import search, password, system

def register_messages_handlers(dp):
    search.register_handlers(dp)
    password.register_handlers(dp)
    system.register_handlers(dp)