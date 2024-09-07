from flask import Flask, render_template, request, redirect, url_for
from fpdf import FPDF
# import hashlib

app = Flask(__name__)

# Grade to point mapping
grade_to_points = {
    'O': 10,
    'A+': 9,
    'A': 8,
    'B+': 7,
    'B':6 ,
    'C': 5,
    'P': 6,
    'F': 0
}

# Sample subjects per semester with credit points
semesters = {
    1: {'Communicative English': 2, 
        'Engineering Chemistry': 3, 
        'Matrices, Differential and Integral Calculus': 4,
        'Programming for problem solving in C':3,
        'Engineering Graphics':4,
        'Chemistry Laboratory':1,
        'C Programming Laboratory':2,
        'Communicative English Laboratory':1},
    
    2: {'Vector Calculus and Complex Functions': 4, 
        'Engineering Physics': 3, 
        'Programming for problem solving using Python': 4,
        'Basic Electrical, Electronics and Communication Engineering':3,
        'Introduction to Information and Computing Technology':3,
        'Constitution of India':0,
        'Physics Laboratory':1,
        'Workshop Practice':2,
        'Basic Electrical, Electronics & Communication Engineering Laboratory':1,
        'Quantitative Aptitude and Verbal Reasoning':1},
    
    
    3: {'Data Structures': 3, 
        'Digital Logic Circuits': 4,
        'Object Oriented Programming ': 3,
        'Computer Architecture ':3,
        ' Discrete Mathematics':4,
        ' Fundamentals of Nano Science':0,
        'Data Structures Laboratory':1,
        'Tamil':1,
        'Object Oriented Programming Laboratory':1,
        'Personality & Character Development':0,
        'Quantitative Aptitude & Behavioral Skills':1},



    4: {'Probability and Statistics': 4, 
        'Operating system': 3, 
        'Design and Analysis of Algorithms': 4,
        'Object Oriented Software Engineering':3,
        'Database Management Systems':3,
        'Java programming':3,
        'Environmental Science and Engineering':0,
        'Operating system Laboratory':1,
        'Database Management Systems Laboratory':1,
        'Java Programming Laboratory':1,
        'Tamil':1,
        'Quantitative Aptitude & Communication Skills':1
        },
    
    5:{
        'Web Technologies':3,
        'Compiler Engineering':4,
        'Data Communication and Networking':3,
        'Professional Ethics and Human Values':3,
        'Professional Elective I':3,
        'Open Elective I':3,
        'Web Technologies Laboratory':1,
        'Data Communication and Networking Laboratory':1,
        ' Quantitative Aptitude and Soft Skills':1
    },
    6:{
        'Computational Intelligence':3,
        'Big Data Analytics':3,
        'Mobile Communication':3,
        'Information Security':3,
        'Professional Elective II':3,
        'Open Elective II':3,
        'Mobile Application Development Laboratory':1,
        'Intelligent System Laboratory':1,
        'Internship':1,
        'Mini Project':1
    },
    7:{
        'Cryptography and Network Security':3,
        'Blockchain Technologies':4,
        'Cloud Computing and Virtualization':3,
        'Professional Elective-III':3,
        'Professional Elective-IV ':3,
        'Open Elective-III':3,
        'Advanced Computing Laboratory':2,
        ' Security Laboratory':2
    },
    8:{
        'Professional Elective-V':3,
        'Professional Elective-VI':3,
        'Project Work':6
    }
    # Add more semesters if needed
}

# Global dictionary to store user's GPA and CGPA
user_results = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        semester_count = int(request.form['semester_count'])
        return redirect(url_for('calculate', semester_count=semester_count))
    return render_template('index.html')

@app.route('/result/<int:semester_count>', methods=['GET', 'POST'])
def calculate(semester_count):
    if request.method == 'POST':
        total_credits = 0
        total_points = 0
        results = {}

        for semester in range(1, semester_count + 1):
            semester_credits = 0
            semester_points = 0
            subjects = []

            for subject, credits in semesters[semester].items():
                grade = request.form[f'sem{semester}_{subject}_grade']
                points = grade_to_points[grade] * credits

                subjects.append((subject, credits, grade))
                semester_credits += credits
                semester_points += points

            gpa = semester_points / semester_credits
            results[semester] = {
                'subjects': subjects,
                'gpa': round(gpa, 2),
                'credits': semester_credits
            }

            total_credits += semester_credits
            total_points += semester_points

        cgpa = total_points / total_credits
        user_results['cgpa'] = round(cgpa, 2)
        user_results['results'] = results

        # # Blockchain hash generation
        # data_string = f"{user_results['cgpa']}{results}"
        # user_results['blockchain_hash'] = hashlib.sha256(data_string.encode()).hexdigest()

        return redirect(url_for('result'))

    return render_template('result.html', semester_count=semester_count, semesters=semesters, grade_to_points=grade_to_points)

@app.route('/marklist')
def result():
    return render_template('marklist.html', 
                           results=user_results['results'], 
                           cgpa=user_results['cgpa'], 
                        #    hash=user_results['blockchain_hash'],
                           grade_to_points=grade_to_points)

@app.route('/download-pdf')
def download_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add the college logo
    pdf.image("static/college_logo.png", x=10, y=8, w=30)

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Academic Marksheet", ln=True, align='C')

    # CGPA
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"CGPA: {user_results['cgpa']}", ln=True, align='C')

    for sem, details in user_results['results'].items():
        pdf.cell(200, 10, txt=f"Semester {sem}", ln=True)
        pdf.cell(90, 10, txt="Subject", border=1)
        pdf.cell(30, 10, txt="Credits", border=1)
        pdf.cell(30, 10, txt="Grade", border=1)
        pdf.cell(30, 10, txt="Points", border=1, ln=True)

        for subject, credits, grade in details['subjects']:
            points = grade_to_points[grade] * credits
            pdf.cell(90, 10, txt=subject, border=1)
            pdf.cell(30, 10, txt=str(credits), border=1)
            pdf.cell(30, 10, txt=grade, border=1)
            pdf.cell(30, 10, txt=str(points), border=1, ln=True)

        pdf.cell(90, 10, txt="GPA", border=1)
        pdf.cell(30, 10, txt="", border=1)
        pdf.cell(30, 10, txt="", border=1)
        pdf.cell(30, 10, txt=str(details['gpa']), border=1, ln=True)

    # Blockchain hash
    # pdf.cell(200, 10, txt=f"Blockchain Verification Hash: {user_results['blockchain_hash']}", ln=True)

    pdf_output = f"{user_results['cgpa']}_CGPA.pdf"
    pdf.output(pdf_output)

    return pdf_output

if __name__ == "__main__":
    app.run(debug=True)
