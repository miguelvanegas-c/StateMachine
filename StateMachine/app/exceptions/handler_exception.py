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
    ActionNotExistError,
    NotInformationError,
)


def register_exception_handlers(app):
    """
    Registra todos los manejadores de excepciones para la aplicación FastAPI.
    Incluye manejo de excepciones personalizadas, HTTP, validación y genéricas.
    """
    
    # =========================================================================
    # 1. VALIDACIÓN DE PYDANTIC (422)
    # =========================================================================
    @app.exception_handler(RequestValidationError)
    async def handler_validation(request: Request, exc: RequestValidationError):
        """
        Maneja errores de validación de Pydantic (body, query params, path params).
        """
        error_response = ErrorResponse(
            status_code=422,
            message="Validation error",
            details=exc.errors()
        ).model_dump()
        return JSONResponse(status_code=422, content=error_response)

    # =========================================================================
    # 2. EXCEPCIONES DE ÓRDENES
    # =========================================================================
    @app.exception_handler(NoOrderException)
    async def handler_noorder(request: Request, exc: NoOrderException):
        """
        Maneja cuando no se encuentra una orden (404).
        """
        error_response = ErrorResponse(
            status_code=404,
            message=str(exc),
            details="There is no order in the DB"
        ).model_dump()
        return JSONResponse(status_code=404, content=error_response)

    @app.exception_handler(InvalidOrderIdError)
    async def handler_invalid_order_id(request: Request, exc: InvalidOrderIdError):
        """
        Maneja IDs de orden inválidos (422) - formato incorrecto de ObjectId.
        """
        error_response = ErrorResponse(
            status_code=422,
            message=str(exc),
            details="Not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"
        ).model_dump()
        return JSONResponse(status_code=422, content=error_response)

    # =========================================================================
    # 3. EXCEPCIONES DE ESTADOS Y EVENTOS
    # =========================================================================
    @app.exception_handler(NoStateError)
    async def handler_nostate(request: Request, exc: NoStateError):
        """
        Maneja cuando no se encuentra un estado (404).
        """
        error_response = ErrorResponse(
            status_code=404,
            message=str(exc),
            details="The requested state does not exist in the system"
        ).model_dump()
        return JSONResponse(status_code=404, content=error_response)

    @app.exception_handler(EventNotExistError)
    async def handler_event_not_exist(request: Request, exc: EventNotExistError):
        """
        Maneja cuando un evento no existe para el estado actual (404).
        """
        error_response = ErrorResponse(
            status_code=404,
            message=str(exc),
            details="The event name is not defined in any state machine"
        ).model_dump()
        return JSONResponse(status_code=404, content=error_response)

    # =========================================================================
    # 4. EXCEPCIONES DE TICKETS
    # =========================================================================
    @app.exception_handler(TicketNotExistError)
    async def handler_ticket_not_exist(request: Request, exc: TicketNotExistError):
        """
        Maneja cuando no se encuentra un ticket para una orden (404).
        """
        error_response = ErrorResponse(
            status_code=404,
            message=str(exc),
            details="The ticket does not exist in the system"
        ).model_dump()
        return JSONResponse(status_code=404, content=error_response)

    # =========================================================================
    # 5. EXCEPCIONES DE REGLAS
    # =========================================================================
    @app.exception_handler(RuleNotExistError)
    async def handler_rule_not_exist(request: Request, exc: RuleNotExistError):
        """
        Maneja cuando no se encuentra una regla para un evento (404).
        """
        error_response = ErrorResponse(
            status_code=404,
            message=str(exc),
            details="The rule for the specified event and name does not exist in the system"
        ).model_dump()
        return JSONResponse(status_code=404, content=error_response)

    @app.exception_handler(RuleExistError)
    async def handler_rule_exist(request: Request, exc: RuleExistError):
        """
        Maneja cuando ya existe una regla con el mismo nombre para un evento (409).
        """
        error_response = ErrorResponse(
            status_code=409,
            message=str(exc),
            details="A rule with the same event name and rule name already exists"
        ).model_dump()
        return JSONResponse(status_code=409, content=error_response)

    # =========================================================================
    # 6. EXCEPCIONES DE ACCIONES
    # =========================================================================
    @app.exception_handler(ActionNotExistError)
    async def handler_action_not_exist(request: Request, exc: ActionNotExistError):
        """
        Maneja cuando una acción no está definida en el sistema (404).
        """
        error_response = ErrorResponse(
            status_code=404,
            message=str(exc),
            details="The action is not defined in the system"
        ).model_dump()
        return JSONResponse(status_code=404, content=error_response)

    # =========================================================================
    # 7. EXCEPCIONES DE INFORMACIÓN
    # =========================================================================
    @app.exception_handler(NotInformationError)
    async def handler_not_information(request: Request, exc: NotInformationError):
        """
        Maneja errores de información faltante o inválida (400).
        """
        error_response = ErrorResponse(
            status_code=400,
            message=str(exc),
            details="Missing or invalid information provided"
        ).model_dump()
        return JSONResponse(status_code=400, content=error_response)

    # =========================================================================
    # 8. EXCEPCIONES DE VALIDACIÓN DE CONDICIONES
    # =========================================================================
    @app.exception_handler(InvalidTypeConditionException)
    async def handler_invalid_type_condition(request: Request, exc: InvalidTypeConditionException):
        """
        Maneja errores de tipo en condiciones de reglas (422).
        """
        error_response = ErrorResponse(
            status_code=422,
            message=str(exc),
            details="The value type does not match the expected type for the condition"
        ).model_dump()
        return JSONResponse(status_code=422, content=error_response)

    # =========================================================================
    # 9. EXCEPCIONES DE CONCURRENCIA
    # =========================================================================
    @app.exception_handler(ConcurrentModificationException)
    async def handler_concurrent_modification(request: Request, exc: ConcurrentModificationException):
        """
        Maneja conflictos de modificación concurrente (409).
        """
        error_response = ErrorResponse(
            status_code=409,
            message=str(exc),
            details="The order was modified by another request. Please refresh and try again."
        ).model_dump()
        return JSONResponse(status_code=409, content=error_response)

    # =========================================================================
    # 10. HTTP EXCEPTIONS (GENÉRICO)
    # =========================================================================
    @app.exception_handler(HTTPException)
    async def handler_http(request: Request, exc: HTTPException):
        """
        Maneja excepciones HTTP genéricas de FastAPI.
        """
        error_response = ErrorResponse(
            status_code=exc.status_code,
            message=exc.detail,
            details="HTTP exception occurred"
        ).model_dump()
        return JSONResponse(status_code=exc.status_code, content=error_response)

    # =========================================================================
    # 11. VALUE ERROR
    # =========================================================================
    @app.exception_handler(ValueError)
    async def handler_value_error(request: Request, exc: ValueError):
        """
        Maneja errores de valor inválido (400).
        """
        error_response = ErrorResponse(
            status_code=400,
            message=str(exc),
            details="Invalid value provided"
        ).model_dump()
        return JSONResponse(status_code=400, content=error_response)

    # =========================================================================
    # 12. TYPE ERROR
    # =========================================================================
    @app.exception_handler(TypeError)
    async def handler_type_error(request: Request, exc: TypeError):
        """
        Maneja errores de tipo (400).
        """
        error_response = ErrorResponse(
            status_code=400,
            message=str(exc),
            details="Invalid type provided"
        ).model_dump()
        return JSONResponse(status_code=400, content=error_response)

    # =========================================================================
    # 13. ATTRIBUTE ERROR
    # =========================================================================
    @app.exception_handler(AttributeError)
    async def handler_attribute_error(request: Request, exc: AttributeError):
        """
        Maneja errores de atributo (500) - normalmente errores de código.
        """
        error_response = ErrorResponse(
            status_code=500,
            message="Internal server error",
            details=f"Attribute error: {str(exc)}"
        ).model_dump()
        return JSONResponse(status_code=500, content=error_response)

    # =========================================================================
    # 14. KEY ERROR
    # =========================================================================
    @app.exception_handler(KeyError)
    async def handler_key_error(request: Request, exc: KeyError):
        """
        Maneja errores de clave faltante en diccionarios (400).
        """
        error_response = ErrorResponse(
            status_code=400,
            message=f"Missing key: {str(exc)}",
            details="Required key not found in the request data"
        ).model_dump()
        return JSONResponse(status_code=400, content=error_response)

    # =========================================================================
    # 15. EXCEPCIONES GENÉRICAS (500)
    # =========================================================================
    @app.exception_handler(Exception)
    async def handler_generic(request: Request, exc: Exception):
        """
        Maneja cualquier excepción no capturada por los handlers anteriores (500).
        """
        # Log del error para debugging
        print(f"❌ Error no manejado: {type(exc).__name__}: {str(exc)}")
        
        error_response = ErrorResponse(
            status_code=500,
            message="Internal server error",
            details="An unexpected error occurred. Please try again later."
        ).model_dump()
        return JSONResponse(status_code=500, content=error_response)

