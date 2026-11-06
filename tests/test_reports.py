"""Unit tests / Модульные тесты для форматирования отчётов."""
from app.reports import table

def test_table_escapes_html():
    result = table(["Field"], [["<script>"]], [12])
    assert "&lt;script&gt;" in result
    assert "<script>" not in result

def test_table_handles_empty():
    result = table(["Name", "Count"], [], [8, 6])
    assert "Name" in result
    assert "Count" in result

def test_table_truncates_long_cells():
    result = table(["Field"], [["123456789"]], [4])
    assert "1234" in result
    assert "12345" not in result
