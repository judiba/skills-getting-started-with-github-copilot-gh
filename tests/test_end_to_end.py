"""Testes end-to-end para workflows completos da API"""

import pytest
from src.app import activities


class TestEndToEndWorkflows:
    """Testes de workflows completos combinando múltiplas operações"""

    def test_signup_then_unregister_workflow(self, client):
        """
        AAA Test: Workflow completo - signup, verificar, unregister, verificar removal
        
        ARRANGE: Preparar email e atividade
        ACT: 1) Fazer signup, 2) Verificar participants, 3) Fazer unregister
        ASSERT: Validar cada etapa do workflow
        """
        # ARRANGE
        email = "workflow_student@mergington.edu"
        activity_name = "Drama Club"
        
        # ACT & ASSERT - Etapa 1: Verificar que email NÃO está inscrito
        assert email not in activities[activity_name]["participants"]
        
        # ACT - Etapa 2: Fazer signup
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT - Etapa 2: Validar signup bem-sucedido
        assert signup_response.status_code == 200
        assert email in activities[activity_name]["participants"]
        
        # ACT - Etapa 3: Fazer unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT - Etapa 3: Validar unregister bem-sucedido
        assert unregister_response.status_code == 200
        assert email not in activities[activity_name]["participants"]

    def test_multiple_signups_different_students(self, client):
        """
        AAA Test: Múltiplas inscrições de estudantes diferentes na mesma atividade
        
        ARRANGE: Preparar emails de múltiplos estudantes
        ACT: Fazer signup de cada estudante na mesma atividade
        ASSERT: Validar que todos foram inscritos
        """
        # ARRANGE
        students = [
            "student1@mergington.edu",
            "student2@mergington.edu",
            "student3@mergington.edu"
        ]
        activity_name = "Debate Club"
        initial_count = len(activities[activity_name]["participants"])
        
        # ACT - Inscrever cada estudante
        responses = []
        for student_email in students:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": student_email}
            )
            responses.append(response)
        
        # ASSERT - Verificar que todos foram inscritos com sucesso
        for response in responses:
            assert response.status_code == 200
        
        for student_email in students:
            assert student_email in activities[activity_name]["participants"]
        
        # ASSERT - Verificar que a contagem de participants aumentou
        final_count = len(activities[activity_name]["participants"])
        assert final_count == initial_count + len(students)

    def test_signup_different_activities_same_student(self, client):
        """
        AAA Test: Mesmo estudante se inscreve em múltiplas atividades diferentes
        
        ARRANGE: Preparar email do estudante e múltiplas atividades
        ACT: Fazer signup do estudante em cada atividade
        ASSERT: Validar que estudante está inscrito em todas
        """
        # ARRANGE
        email = "multi_activity_student@mergington.edu"
        activities_to_join = ["Science Club", "Art Club", "Debate Club"]
        
        # ACT - Inscrever em cada atividade
        responses = []
        for activity_name in activities_to_join:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            responses.append(response)
        
        # ASSERT - Verificar que todos os signups foram bem-sucedidos
        for i, response in enumerate(responses):
            assert response.status_code == 200
        
        # ASSERT - Verificar que estudante está inscrito em todas as atividades
        for activity_name in activities_to_join:
            assert email in activities[activity_name]["participants"]
