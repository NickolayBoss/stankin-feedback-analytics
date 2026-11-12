"""Lightweight offline checks; integration tests run against PostgreSQL in CI."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_demo_schema_has_integrity_constraints():
    schema = (ROOT / "sql/00_demo_schema.sql").read_text()
    assert "REFERENCES departments" in schema
    assert "CHECK(" in schema
    assert "CREATE INDEX" in schema

def test_kpi_has_safe_denominators():
    sql = (ROOT / "sql/03_analytics.sql").read_text()
    assert "nullif(" in sql.lower()
    assert "percentile_cont" in sql.lower()

def test_trend_uses_window_function():
    sql = (ROOT / "sql/04_trends.sql").read_text()
    assert "lag(" in sql.lower()

def test_no_real_data_in_seed():
    sql = (ROOT / "sql/02_seed.sql").read_text()
    assert "generate_series(0,499)" in sql
