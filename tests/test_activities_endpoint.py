"""Testes para o endpoint GET /activities"""

import pytest


class TestGetActivities:
    """Testes de integração para o endpoint GET /activities"""

    def test_get_activities_returns_all_activities(self, client):
        """
        AAA Test: Verificar se GET /activities retorna todas as 9 atividades
        
        ARRANGE: Preparar cliente de teste
        ACT: Fazer requisição GET /activities
        ASSERT: Validar que temos 9 atividades na resposta
        """
        # ARRANGE
        # (client já vem da fixture conftest.py)
        
        # ACT
        response = client.get("/activities")
        
        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
        assert "Basketball Team" in data
        assert "Soccer Club" in data
        assert "Art Club" in data
        assert "Drama Club" in data
        assert "Debate Club" in data
        assert "Science Club" in data

    def test_get_activities_status_code_200(self, client):
        """
        AAA Test: Verificar se status code é 200
        
        ARRANGE: Preparar cliente de teste
        ACT: Fazer requisição GET /activities
        ASSERT: Validar status code 200
        """
        # ARRANGE
        # (client já vem da fixture conftest.py)
        
        # ACT
        response = client.get("/activities")
        
        # ASSERT
        assert response.status_code == 200

    def test_get_activities_response_structure(self, client):
        """
        AAA Test: Verificar estrutura de resposta (dados esperados por atividade)
        
        ARRANGE: Preparar cliente de teste e atividades esperadas
        ACT: Fazer requisição GET /activities
        ASSERT: Validar que cada atividade tem campos obrigatórios
        """
        # ARRANGE
        expected_keys = {"description", "schedule", "max_participants", "participants"}
        
        # ACT
        response = client.get("/activities")
        data = response.json()
        
        # ASSERT
        for activity_name, activity_data in data.items():
            assert isinstance(activity_name, str)
            assert isinstance(activity_data, dict)
            assert set(activity_data.keys()) == expected_keys
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)
