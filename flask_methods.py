import json
from flask import Flask, render_template, url_for, jsonify, abort, make_response, request, redirect


app = Flask(__name__, template_folder="templates")  # create flask app


with open("student.json","r") as f :    # load data
    students = json.load(f)


@app.route('/')
@app.route("/home")
@app.route("/index")
def index():
    return render_template("index.html")   

@app.route('/Students')
def get_students():
    return make_response(
        jsonify({'student': students}),
        200
    )

@app.route('/Students/<string:name>')
def get_student(name):
    student = [student for student in students if student['name'] == name]
    if len(student) == 0 :
        abort(404)
    return make_response(
        jsonify({'student': student[0]}),
        200
    )

@app.route('/Students', methods=['POST'])   
def create_student():
    if not request.json or not 'name' in request.json:
        abort(400)
    new_student = request.get_json(force=True)
    students.append(new_student)

    return redirect(url_for('get_students'))  # return all students

@app.route('/Students/<string:name>', methods=['PUT'])
def update_student(name):
    if not request.json:
        abort(400)

    student = [student for student in students if student['name'] == name]
    if len(student) == 0 :
        abort(404)

    for index, student in enumerate(students):
        if student['name'] == name :
            students[index] = request.get_json(force=True)
    
    return redirect(url_for('get_students'))  # return all students

@app.route('/Students/<string:name>', methods=['DELETE'])
def delete_student(name):
    student = [student for student in students if student['name'] == name]
    print(student)
    if len(student) == 0 :
        abort(404)
    students.remove(student[0])
    return redirect(url_for('get_students'))  # return all students









@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({'error': 'Internal server error'}), 500)

if __name__ == '__main__' :
    app.run()