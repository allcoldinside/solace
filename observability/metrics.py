"""Prometheus metrics."""

from __future__ import annotations

from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter("solace_http_requests_total", "HTTP requests", ["method", "path", "status"])
REQUEST_DURATION = Histogram("solace_http_request_duration_seconds", "HTTP request duration", ["method", "path"])
PIPELINE_SUCCESS = Counter("solace_pipeline_success_total", "Successful pipeline runs")
PIPELINE_FAILURE = Counter("solace_pipeline_failure_total", "Failed pipeline runs")
PIPELINE_DURATION = Histogram("solace_pipeline_duration_seconds", "Pipeline duration")
PANEL_TURNS = Counter("solace_panel_turns_total", "Panel turns")


def metrics_response() -> bytes:
    return generate_latest()
