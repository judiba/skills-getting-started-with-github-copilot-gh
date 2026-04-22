"""Fixtures compartilhadas para todos os testes"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Fixture que retorna um TestClient para a app FastAPI"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture que reseta o estado das atividades ANTES e DEPOIS de cada teste.
    autouse=True significa que roda automaticamente em todos os testes.
    Garante isolamento entre testes - cada teste começa com estado limpo.
    """
    # Dados iniciais de atividades conforme definido em src/app.py
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Practice basketball skills and compete in local leagues",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": []
        },
        "Soccer Club": {
            "description": "Learn soccer techniques and play matches",
            "schedule": "Wednesdays and Fridays, 3:00 PM - 4:30 PM",
            "max_participants": 22,
            "participants": []
        },
        "Art Club": {
            "description": "Express creativity through painting, drawing, and other art forms",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 10,
            "participants": []
        },
        "Drama Club": {
            "description": "Participate in theater productions and improve acting skills",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 12,
            "participants": []
        },
        "Debate Club": {
            "description": "Develop argumentation and public speaking skills through debates",
            "schedule": "Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 8,
            "participants": []
        },
        "Science Club": {
            "description": "Explore scientific concepts and conduct experiments",
            "schedule": "Fridays, 2:00 PM - 3:30 PM",
            "max_participants": 15,
            "participants": []
        }
    }
    
    # Limpar dicionário e recarregar dados originais ANTES do teste
    activities.clear()
    activities.update(original_activities)
    
    yield  # ← Teste roda aqui
    
    # Cleanup DEPOIS do teste (garante limpeza)
    activities.clear()
    activities.update(original_activities)
