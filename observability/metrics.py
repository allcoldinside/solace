from prometheus_client import Counter, Histogram, generate_latest

pipeline_success = Counter('solace_pipeline_success_total', 'pipeline success count')
pipeline_failure = Counter('solace_pipeline_failure_total', 'pipeline failure count')
pipeline_duration = Histogram('solace_pipeline_duration_seconds', 'pipeline duration seconds')
panel_turn_counter = Counter('solace_panel_turn_total', 'panel turn count')


def render_metrics() -> bytes:
    return generate_latest()
