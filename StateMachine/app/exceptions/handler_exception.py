from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.schemas.response_schemas import ErrorResponse
from app.exceptions.exceptions import (
    NoOrderException,
    InvalidOrderIdError,
    NoStateError,
    EventNotExistError,
    TicketNotExistError,
    ConcurrentModificationException,
    InvalidTypeConditionException,
    RuleNotExistError,
    RuleExistError,
    ActionNotExistError,  # ✅ Nueva excepción
)


def register_exception_handlers(app):
    """
    Registra todos los manejadores de excepciones para la aplicación.
    """
    
    # ============ 1. Validación de Pydantic ============
    @app.exception_handler(RequestValidationError)
    async def handler_validation(request: Request, exc: RequestValidationError):
        error_response = ErrorResponse(
            status_code=422,
            message="Validation error",
            details=exc.errors()
        ).model_dump()
        return JSONResponse(status_code=422, content=error_response)

    # ============ 2. Excepciones de Órdenes (404) ============
    @app.exception_handler(NoOrderException)
    async def handler_noorder(request: Request, exc: NoOrderException):
        error_response = ErrorResponse(
            status_code=404,
            message=str(exc),
            details="There is no order in the DB"
        ).model_dump()
        return JSONResponse(status_code=404, content=error_response)

    @app.exception_handler(InvalidOrderIdError)
    async def handler_invalid_order_id(request: Request, exc: InvalidOrderIdError):
        error_response = ErrorResponse(
            status_code=422,
            message=str(exc),
            details="Not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"
        ).model_dump()
        return JSONResponse(status_code=422, content=error_response)

    # ============ 3. Excepciones de Estados y Eventos (404) ============
    @app.exception_handler(NoStateError)
    async def handler_nostate(request: Request, exc: NoStateError):
        error_response = ErrorResponse(
            status_code=404,
            message=str(exc),
            details="The requested state does not exist in the system"
        ).model_dump()
        return JSONResponse(status_code=404, content=error_response)

    @app.exception_handler(EventNotExistError)
    async def handler_event_not_exist(request: Request, exc: EventNotExistError):
        error_response = ErrorResponse(
            status_code=404,
            message=str(exc),
            details="The event name is not defined in any state machine"
        ).model_dump()
        return JSONResponse(status_code=404, content=error_response)

    # ============ 4. Excepciones de Tickets (404) ============
    @app.exception_handler(TicketNotExistError)
    async def handler_ticket_not_exist(request: Request, exc: TicketNotExistError):
        error_response = ErrorResponse(
            status_code=404,
            message=str(exc),
            details="The ticket does not exist in the system"
        ).model_dump()
        return JSONResponse(status_code=404, content=error_response)

    # ============ 5. Excepciones de Reglas (404 y 409) ============
    @app.exception_handler(RuleNotExistError)
    async def handler_rule_not_exist(request: Request, exc: RuleNotExistError):
        error_response = ErrorResponse(
            status_code=404,
            message=str(exc),
            details="The rule for the specified event and name does not exist in the system"
        ).model_dump()
        return JSONResponse(status_code=404, content=error_response)

    @app.exception_handler(RuleExistError) 
    async def handler_rule_exist(request: Request, exc: RuleExistError):
        error_response = ErrorResponse(
            status_code=409,  # Conflict
            message=str(exc),
            details="A rule with the same event name and rule name already exists"
        ).model_dump()
        return JSONResponse(status_code=409, content=error_response)

    # ============ 6. Excepciones de Acciones (404) ============
    @app.exception_handler(ActionNotExistError)  
    async def handler_action_not_exist(request: Request, exc: ActionNotExistError):
        error_response = ErrorResponse(
            status_code=404,
            message=str(exc),
            details="The action is not defined in the system"
        ).model_dump()
        return JSONResponse(status_code=404, content=error_response)

    # ============ 7. Excepciones de Validación de Condiciones (422) ============
    @app.exception_handler(InvalidTypeConditionException)
    async def handler_invalid_type_condition(request: Request, exc: InvalidTypeConditionException):
        error_response = ErrorResponse(
            status_code=422,
            message=str(exc),
            details="The value type does not match the expected type for the condition"
        ).model_dump()
        return JSONResponse(status_code=422, content=error_response)

    # ============ 8. Excepciones de Concurrencia (409) ============
    @app.exception_handler(ConcurrentModificationException)
    async def handler_concurrent_modification(request: Request, exc: ConcurrentModificationException):
        error_response = ErrorResponse(
            status_code=409,
            message=str(exc),
            details="The order was modified by another request. Please refresh and try again."
        ).model_dump()
        return JSONResponse(status_code=409, content=error_response)

    # ============ 9. HTTP Exceptions (Genérico) ============
    @app.exception_handler(HTTPException)
    async def handler_http(request: Request, exc: HTTPException):
        error_response = ErrorResponse(
            status_code=exc.status_code,
            message=exc.detail,
            details="HTTP exception occurred"
        ).model_dump()
        return JSONResponse(status_code=exc.status_code, content=error_response)

    # ============ 10. ValueError (400) ============
    @app.exception_handler(ValueError)
    async def handler_value_error(request: Request, exc: ValueError):
        error_response = ErrorResponse(
            status_code=400,
            message=str(exc),
            details="Invalid value provided"
        ).model_dump()
        return JSONResponse(status_code=400, content=error_response)

    # ============ 11. Excepciones Genéricas (500) ============
    @app.exception_handler(Exception)
    async def handler_generic(request: Request, exc: Exception):
        # Log del error para debugging
        print(f"❌ Error no manejado: {type(exc).__name__}: {str(exc)}")
        
        error_response = ErrorResponse(
            status_code=500,
            message="Internal server error",
            details="An unexpected error occurred. Please try again later."
        ).model_dump()
        return JSONResponse(status_code=500, content=error_response)