"""Testes para o endpoint DELETE /activities/{activity_name}/signup"""

import pytest


class TestUnregisterEndpoint:
    """Testes de integração para o endpoint DELETE unregister"""

    def test_unregister_success(self, client):
        """
        AAA Test: DELETE remove email da lista de participants
        
        ARRANGE: Preparar email que está inscrito
        ACT: Fazer DELETE request para unregister
        ASSERT: Validar que email foi removido
        """
        # ARRANGE
        email = "michael@mergington.edu"  # Já inscrito em Chess Club
        activity_name = "Chess Club"
        from src.app import activities
        initial_count = len(activities[activity_name]["participants"])
        
        # ACT
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count - 1

    def test_unregister_returns_200(self, client):
        """
        AAA Test: Validar status code 200 no unregister bem-sucedido
        
        ARRANGE: Preparar email que está inscrito
        ACT: Fazer DELETE request para unregister
        ASSERT: Validar status code é 200
        """
        # ARRANGE
        email = "daniel@mergington.edu"  # Já inscrito em Chess Club
        activity_name = "Chess Club"
        
        # ACT
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 200

    def test_unregister_success_response_message(self, client):
        """
        AAA Test: Validar mensagem de resposta no unregister bem-sucedido
        
        ARRANGE: Preparar email que está inscrito
        ACT: Fazer DELETE request para unregister
        ASSERT: Validar que mensagem contém "Unregistered"
        """
        # ARRANGE
        email = "emma@mergington.edu"  # Já inscrito em Programming Class
        activity_name = "Programming Class"
        
        # ACT
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # ASSERT
        assert "message" in data
        assert "Unregistered" in data["message"]
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_unregister_not_signed_up_fails(self, client):
        """
        AAA Test: Tentar deletar alguém não inscrito retorna status 400
        
        ARRANGE: Preparar email que NÃO está inscrito em uma atividade
        ACT: Fazer DELETE request para unregister
        ASSERT: Validar status code é 400
        """
        # ARRANGE
        email = "student_not_registered@mergington.edu"  # Não está inscrito
        activity_name = "Chess Club"
        
        # ACT
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 400

    def test_unregister_not_signed_up_error_message(self, client):
        """
        AAA Test: Validar mensagem de erro para aluno não inscrito
        
        ARRANGE: Preparar email que NÃO está inscrito
        ACT: Fazer DELETE request para unregister
        ASSERT: Validar que mensagem contém "not signed up"
        """
        # ARRANGE
        email = "not_signed_up@mergington.edu"
        activity_name = "Basketball Team"
        
        # ACT
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # ASSERT
        assert response.status_code == 400
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()

    def test_unregister_invalid_activity_fails(self, client):
        """
        AAA Test: DELETE em atividade inexistente retorna status 404
        
        ARRANGE: Preparar email e atividade inválida
        ACT: Fazer DELETE request para atividade que não existe
        ASSERT: Validar status code é 404
        """
        # ARRANGE
        email = "student@mergington.edu"
        activity_name = "Nonexistent Club"
        
        # ACT
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 404

    def test_unregister_invalid_activity_error_message(self, client):
        """
        AAA Test: Validar mensagem de erro para atividade inválida
        
        ARRANGE: Preparar email e atividade inválida
        ACT: Fazer DELETE request para atividade que não existe
        ASSERT: Validar que mensagem contém "not found"
        """
        # ARRANGE
        email = "student@mergington.edu"
        activity_name = "Invalid Activity"
        
        # ACT
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # ASSERT
        assert response.status_code == 404
        assert "detail" in data
        assert "not found" in data["detail"].lower()
