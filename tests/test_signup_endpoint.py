"""Testes para o endpoint POST /activities/{activity_name}/signup"""

import pytest


class TestSignupEndpoint:
    """Testes de integração para o endpoint POST signup"""

    def test_signup_success(self, client):
        """
        AAA Test: Signup bem-sucedido adiciona email à lista de participants
        
        ARRANGE: Preparar email e atividade
        ACT: Fazer POST request para signup
        ASSERT: Validar que email foi adicionado
        """
        # ARRANGE
        email = "newstudent@mergington.edu"
        activity_name = "Basketball Team"
        
        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 200
        from src.app import activities
        assert email in activities[activity_name]["participants"]

    def test_signup_returns_200(self, client):
        """
        AAA Test: Validar status code 200 no signup bem-sucedido
        
        ARRANGE: Preparar email e atividade
        ACT: Fazer POST request para signup
        ASSERT: Validar status code é 200
        """
        # ARRANGE
        email = "newstudent@mergington.edu"
        activity_name = "Soccer Club"
        
        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 200

    def test_signup_success_response_message(self, client):
        """
        AAA Test: Validar mensagem de resposta no signup bem-sucedido
        
        ARRANGE: Preparar email e atividade
        ACT: Fazer POST request para signup
        ASSERT: Validar que mensagem contém "Signed up"
        """
        # ARRANGE
        email = "newstudent@mergington.edu"
        activity_name = "Art Club"
        
        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # ASSERT
        assert "message" in data
        assert "Signed up" in data["message"]
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_duplicate_email_fails(self, client):
        """
        AAA Test: Tentar signup do mesmo email 2x retorna status 400
        
        ARRANGE: Preparar email que já está inscrito em Chess Club
        ACT: Fazer POST request para signup do mesmo email
        ASSERT: Validar status code é 400
        """
        # ARRANGE
        email = "michael@mergington.edu"  # Já inscrito em Chess Club
        activity_name = "Chess Club"
        
        # ACT - Tentar signup novamente com mesmo email
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 400

    def test_signup_duplicate_email_error_message(self, client):
        """
        AAA Test: Validar mensagem de erro para email duplicado
        
        ARRANGE: Preparar email que já está inscrito
        ACT: Fazer POST request para signup do mesmo email
        ASSERT: Validar que mensagem contém "already signed up"
        """
        # ARRANGE
        email = "daniel@mergington.edu"  # Já inscrito em Chess Club
        activity_name = "Chess Club"
        
        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # ASSERT
        assert response.status_code == 400
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_invalid_activity_fails(self, client):
        """
        AAA Test: Signup em atividade inexistente retorna status 404
        
        ARRANGE: Preparar email e atividade inválida
        ACT: Fazer POST request para atividade que não existe
        ASSERT: Validar status code é 404
        """
        # ARRANGE
        email = "student@mergington.edu"
        activity_name = "Nonexistent Club"
        
        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 404

    def test_signup_invalid_activity_error_message(self, client):
        """
        AAA Test: Validar mensagem de erro para atividade inválida
        
        ARRANGE: Preparar email e atividade inválida
        ACT: Fazer POST request para atividade que não existe
        ASSERT: Validar que mensagem contém "not found"
        """
        # ARRANGE
        email = "student@mergington.edu"
        activity_name = "Invalid Activity"
        
        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # ASSERT
        assert response.status_code == 404
        assert "detail" in data
        assert "not found" in data["detail"].lower()
