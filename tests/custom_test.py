from core.models.assignments import AssignmentStateEnum, GradeEnum
import json
def test_get_ready_state(client):
    response = client.get(
        '/'
    )

    assert response.status_code == 200

    content = response.json['status']
    assert content == 'ready'


def test_create_new_assignment(client, h_student_1):
    content = 'a new assignment'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_update_new_assignment(client, h_student_1):
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id': 6,
            'content': 'a new updated assignment'
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_new_assignment(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 6,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_teacher_grade_new_assignment(client, h_teacher_2):
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            'id': 6,
            'grade': "A"
        })
    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.A


def test_teacher_list_from_principal(client, h_principal):
    response = client.get(
        '/principal/teachers',
        headers=h_principal,
        )
    
    assert response.status_code == 200


def test_get_integrety_err(client):
    content = 'should raise integrety error'

    response = client.post(
        '/student/assignments',
        headers={
            'X-Principal': json.dumps({
                'student_id': 200,
                'user_id': 200
            })
        },
        json={
            'content': content
        })

    assert response.status_code == 400
    assert response.json['error'] == "IntegrityError"