from flask import Blueprint, request, jsonify
from app.models import db, Group, Student, Course

api_bp = Blueprint('api', __name__)


@api_bp.route('/groups', methods=['POST'])
def add_group():
    data = request.get_json()
    group = Group(name=data['name'])
    db.session.add(group)
    db.session.commit()
    return jsonify({'id': group.id, 'name': group.name}), 201


@api_bp.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    student = Student(group_id=data['group_id'], first_name=data['first_name'], last_name=data['last_name'])
    db.session.add(student)
    db.session.commit()
    return jsonify({'id': student.id, 'group_id': student.group_id, 'first_name': student.first_name, 'last_name': student.last_name}), 201


@api_bp.route('/courses', methods=['POST'])
def add_course():
    data = request.get_json()
    course = Course(name=data['name'], description=data['description'])
    db.session.add(course)
    db.session.commit()
    return jsonify({'id': course.id, 'name': course.name, 'description': course.description}), 201


@api_bp.route('/students/<int:student_id>/courses', methods=['POST'])
def add_student_to_course(student_id):
    data = request.get_json()
    student = Student.query.get(student_id)
    course = Course.query.get(data['course_id'])
    student.courses.append(course)
    db.session.commit()
    return jsonify({'student_id': student.id, 'course_id': course.id}), 200


@api_bp.route('/students/courses/<course_name>', methods=['GET'])
def get_students_by_course(course_name):
    course = Course.query.filter_by(name=course_name).first()
    if course:
        students = course.students
        return jsonify([{'id': student.id, 'group_id': student.group_id, 'first_name': student.first_name, 'last_name': student.last_name} for student in students]), 200
    return jsonify({'message': 'Course not found'}), 404


@api_bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': 'Student deleted successfully'}), 200
    return jsonify({'message': 'Student not found'}), 404


@api_bp.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    student = Student.query.get(student_id)
    if student:
        student.group_id = data['group_id']
        student.first_name = data['first_name']
        student.last_name = data['last_name']
        db.session.commit()
        return jsonify({'id': student.id, 'group_id': student.group_id, 'first_name': student.first_name, 'last_name': student.last_name}), 200
    return jsonify({'message': 'Student not found'}), 404


@api_bp.route('/groups/students_count/<int:max_students>', methods=['GET'])
def get_groups_by_student_count(max_students):
    groups = Group.query.all()
    result = []
    for group in groups:
        student_count = len(group.students)
        if student_count <= max_students:
            result.append({'id': group.id, 'name': group.name})
    return jsonify(result), 200


@api_bp.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get(course_id)
    if course:
        db.session.delete(course)
        db.session.commit()
        return jsonify({'message': 'Course deleted successfully'}), 200
    return jsonify({'message': 'Course not found'}), 404
