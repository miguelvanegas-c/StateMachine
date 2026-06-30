

from app.exceptions.exceptions import ActionNotExistError


class ActionService:

    def __init__(self):
        self.actions: dict[str, callable] = {
            "TICKET": self.ticket_action
        }

    def validate_action(self, action:str):
       if action not in self.actions:
            raise ActionNotExistError(action)
    
    async def execute_action(self, action:str, order, metadata:dict):
        self.validate_action(action)
        action_function = self.actions[action]
        await action_function(order, metadata)

    async def ticket_action(self, order, metadata:dict):
        pass

    