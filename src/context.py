from contextvars import ContextVar

TRACE_ID: ContextVar[str] = ContextVar("TRACE_ID", default="unknown")
