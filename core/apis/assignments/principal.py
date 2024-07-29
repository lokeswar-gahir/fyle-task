from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from sqlalchemy import select

from .schema import AssignmentSchema, AssignmentGradeSchema, TeacherSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'])
@decorators.authenticate_principal
def list_submitted_and_graded(p):
    submitted_or_graded = Assignment.get_sumbitted_or_graded()
    sg_assignments_dump = AssignmentSchema().dump(submitted_or_graded, many=True)
    # print(submitted_or_graded)
    return APIResponse.respond(data=sg_assignments_dump)


@principal_assignments_resources.route('/teachers', methods=['GET'])
@decorators.authenticate_principal
def list_teachers(p):
    r = Teacher.query.all()
    teacher_result_dump = TeacherSchema().dump(r, many=True)
    # print(teacher_result_dump)
    return APIResponse.respond(data=teacher_result_dump)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_or_regrade_assignments(p, incoming_payload):
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)

