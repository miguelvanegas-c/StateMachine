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