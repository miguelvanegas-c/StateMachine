class NoOrderException(Exception):
    def __init__(self, order_id: str | None):
        if order_id is None:
            super().__init__("No orders found")
        else:
            super().__init__(f"The order_id '{order_id}' is invalid")

class StrategyNotFoundError(Exception):
    def __init__(self, name: str):
        super().__init__(f"The action with name '{name}' not exists")

class OperatorNotFoundError(Exception):
    def __init__(self, name: str):
        super().__init__(f"The operator with name '{name}' not exists")

class FactoryNotFoundError(Exception):
    def __init__(self, name: str):
        super().__init__(f"The rule type with name '{name}' not exists")

class InvalidOrderIdError(Exception):
    def __init__(self, order_id: str):
        super().__init__(f"The order_id '{order_id}' is invalid")


class NoStateError(Exception):
    def __init__(self, state: str |None):
        if state is None:
            super().__init__("No states found")
        else:
            super().__init__(f"The state {state}, not exist")


class EventInvalidError(Exception):
    def __init__(self, event: str, state: str):
        super().__init__(f"The state {state}, can't manage the {event} event")


class EventNotExistError(Exception):
    def __init__(self, event: str|None):
        if event is None:
            super().__init__("No events found")
        else:
            super().__init__(f"The event {event} does not exist")


class TicketNotExistError(Exception):
    def __init__(self, order: str | None):
        if order is None:
            super().__init__("No tickets found")
        else:
            super().__init__(f"The ticket to order id {order}, not exist")


class ConcurrentModificationException(Exception):
    def __init__(self):
        super().__init__(f"The operation has been done by another process. Please try again.")