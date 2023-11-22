import math
from flask import Flask, render_template, request, jsonify,redirect,url_for,Response,flash
import os
from flask_mysqldb import MySQL
import warnings
import utils
import time
import cv2

#variables
studentInfo=None
camera=None
profileName=None

#Flak's Application Confguration
warnings.filterwarnings("ignore")
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'xyz'
os.path.dirname("../templates")

#Flak's Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'examproctordb'
mysql = MySQL(app)

#Function to show face detection's Rectangle in Face Input Page
def capture_by_frames():
    global camera
    utils.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        success, frame = utils.cap.read()  # read the camera frame
        detector=cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
        faces=detector.detectMultiScale(frame,1.2,6)
         #Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#Function to run Cheat Detection when we start run the Application
@app.before_request
def start_loop():
    pass

#Login Related
@app.route('/')
def main():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    global studentInfo
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students where Email='" + username + "' and Password='" + password + "'")
        data = cur.fetchone()
        if data is None:
            flash('Your Email or Password is incorrect, try again.', category='error')
            return redirect(url_for('main'))
        else:
            id, name, email,password, role = data
            studentInfo={ "Id": id, "Name": name, "Email": email, "Password": password}
            if role == 'STUDENT':
                utils.Student_Name = name
                return redirect(url_for('rules'))
            else:
                return redirect(url_for('adminStudents'))

@app.route('/logout')
def logout():
    return render_template('login.html')

#Student Related
@app.route('/rules')
def rules():
    return render_template('ExamRules.html')

@app.route('/faceInput')
def faceInput():
    return render_template('ExamFaceInput.html')

@app.route('/video_capture')
def video_capture():
    return Response(capture_by_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/saveFaceInput')
def saveFaceInput():
    global profileName
    if utils.cap.isOpened():
        utils.cap.release()
    cam = cv2.VideoCapture(0)
    success, frame = cam.read()  # read the camera frame
    profileName=f"{studentInfo['Name']}_{utils.get_resultId():03}" + "Profile.jpg"
    cv2.imwrite(profileName,frame)
    utils.move_file_to_output_folder(profileName,'Profiles')
    cam.release()
    return redirect(url_for('confirmFaceInput'))

@app.route('/confirmFaceInput')
def confirmFaceInput():
    profile = profileName
  #  utils.fr.encode_faces()
    return render_template('ExamConfirmFaceInput.html', profile = profile)

@app.route('/systemCheck')
def systemCheck():
    return render_template('ExamSystemCheck.html')

@app.route('/systemCheck', methods=["POST"])
def systemCheckRoute():
    if request.method == 'POST':
        examData = request.json
        output = 'exam'
        if 'Not available' in examData['input'].split(';'): output = 'systemCheckError'
    return jsonify({"output": output})

@app.route('/systemCheckError')
def systemCheckError():
    return render_template('ExamSystemCheckError.html')

@app.route('/exam')
def exam():
    return render_template('Exam.html')

@app.route('/exam', methods=["POST"])
def examAction():
    link = ''
    if request.method == 'POST':
        examData = request.json
        if(examData['input']!=''):
            totalMark=  math.floor(float(examData['input'])* 6.6667)
            if totalMark < 50:
                status="Fail"
                link = 'showResultFail'
            else:
                status="Pass"
                link = 'showResultPass'
            utils.write_json({
                "Id": utils.get_resultId(),
                "Name": studentInfo['Name'],
                "TotalMark": totalMark,
                "Status": status,
                "Date": time.strftime("%Y-%m-%d", time.localtime(time.time())),
                "StId": studentInfo['Id'],
                "Link" : profileName
            },"result.json")
            resultStatus= studentInfo['Name']+';'+str(totalMark)+';'+status+';'+time.strftime("%Y-%m-%d", time.localtime(time.time()))
        else:
            resultStatus=''
    return jsonify({"output": resultStatus, "link": link})

@app.route('/showResultPass/<result_status>')
def showResultPass(result_status):
    return render_template('ExamResultPass.html',result_status=result_status)

@app.route('/showResultFail/<result_status>')
def showResultFail(result_status):
    return render_template('ExamResultFail.html',result_status=result_status)

#Admin Related
@app.route('/adminResults')
def adminResults():
    results = utils.getResults()
    return render_template('Results.html', results=results)

@app.route('/adminStudents')
def adminStudents():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students where Role='STUDENT'")
    data = cur.fetchall()
    cur.close()
    return render_template('Students.html', students=data)

@app.route('/insertStudent', methods=['POST'])
def insertStudent():
    if request.method == "POST":
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (Name, Email, Password, Role) VALUES (%s, %s, %s, %s)", (name, email, password,'STUDENT'))
        mysql.connection.commit()
        return redirect(url_for('adminStudents'))

@app.route('/deleteStudent/<string:stdId>', methods=['GET'])
def deleteStudent(stdId):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE ID=%s", (stdId,))
    mysql.connection.commit()
    return redirect(url_for('adminStudents'))

@app.route('/updateStudent', methods=['POST', 'GET'])
def updateStudent():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE students
               SET Name=%s, Email=%s, Password=%s
               WHERE ID=%s
            """, (name, email, password, id_data))
        mysql.connection.commit()
        return redirect(url_for('adminStudents'))

if __name__ == '__main__':
    app.run(debug=True)