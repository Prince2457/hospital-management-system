import pytest
import unittest.mock as mock
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.appointments import check_doctor_availability
def test_doctor_not_available():
    result = check_doctor_availability(1, "2026-03-15", "10:00:00")
    assert result == False

def test_doctor_availability():
    result = check_doctor_availability(1, "2026-04-1", "9:00:00")
    assert result == True

vmf