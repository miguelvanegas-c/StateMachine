class NoOrderException(Exception):
    def __init__(self, order_id: str | None):
        if order_id is None:
            super().__init__("No orders found")
        else:
            super().__init__(f"The order '{order_id}' was not found")


class InvalidOrderIdError(Exception):
    def __init__(self, order_id: str):
        super().__init__(f"The order_id '{order_id}' is invalid")


class NoStateError(Exception):
    def __init__(self, state: str | None):
        if state is None:
            super().__init__("No states found")
        else:
            super().__init__(f"The state '{state}' does not exist")


class EventNotExistError(Exception):
    def __init__(self, event: str | None):
        if event is None:
            super().__init__("No events found")
        else:
            super().__init__(f"The event '{event}' is not valid for the current state")


class ConcurrentModificationException(Exception):
    def __init__(self):
        super().__init__("The order was modified by another process. Please try again.")


class TicketNotExistError(Exception):
    def __init__(self, order_id: str | None):
        if order_id is None:
            super().__init__("No tickets found")
        else:
            super().__init__(f"No ticket found for order '{order_id}'")

class InvalidTypeConditionException(Exception):
    def __init__(self, field: str, expected_type: str):
        super().__init__(f"The value for '{field}' must be of type '{expected_type}'")


class RuleNotExistError(Exception):
    def __init__(self, event_name: str, name: str):
        super().__init__(f"The rule for event '{event_name}' and name '{name}' does not exist")

class ActionNotExistError(Exception):
    def __init__(self, action: str):
        super().__init__(f"The action '{action}' does not exist")

class RuleExistError(Exception):
    def __init__(self, event_name: str, name: str):
        if name is None:
            super().__init__(f"The rule for event '{event_name}' already exists")
        else:       
            super().__init__(f"The rule for event '{event_name}' and name '{name}' already exists")