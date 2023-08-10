from flask import Flask, render_template, request
import os
import re
from collections import Counter

def preprocess_text(text):
    # Remove non-alphanumeric characters and convert to lowercase
    text = re.sub(r'\W+', ' ', text).lower()
    return text

def calculate_matching_percentage(job_description_file, resume_file):
    encodings = ['utf-8', 'latin-1', 'cp1252', 'ISO-8859-1']

    for encoding in encodings:
        try:
            # Step 1: Read the content of both files with the specified encoding
            with open(job_description_file, 'r', encoding=encoding) as file:
                job_description_content = file.read()
            with open(resume_file, 'r', encoding=encoding) as file:
                resume_content = file.read()

            # Step 2: Preprocess the text data
            job_description_words = preprocess_text(job_description_content).split()
            resume_words = preprocess_text(resume_content).split()

            # Step 3: Find the set of unique keywords from the job description
            job_description_keywords = set(job_description_words)

            # Step 4: Count the number of matching keywords
            matching_keywords_count = sum(1 for word in resume_words if word in job_description_keywords)

            # Step 5: Calculate the percentage of matching keywords
            total_keywords_in_resume_resume = len(resume_words)
            matching_percentage = (matching_keywords_count / total_keywords_in_resume_resume) * 100

            return matching_percentage

        except UnicodeDecodeError:
            continue

def check_multiple_resumes(job_description_file, resume_files):
    results = []

    for resume_file in resume_files:
        matching_percentage = calculate_matching_percentage(job_description_file, resume_file)
        if matching_percentage is not None:
            results.append((resume_file, matching_percentage))

    return results

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_word():
    return render_template('index.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        # Get the uploaded files from the request object
        job_description_file = request.files['job_description']
        resume_files = request.files.getlist('resume')  # Get a list of uploaded resume files

        # Save the uploaded files to a temporary directory
        job_description_path = os.path.join('files', job_description_file.filename)
        job_description_file.save(job_description_path)

        resume_paths = []  # A list to store the temporary paths of the uploaded resume files

        for resume_file in resume_files:
            resume_path = os.path.join('files', resume_file.filename)
            resume_file.save(resume_path)
            resume_paths.append(resume_path)

        # Get the desired matching percentage from the user input
        desired_percentage = float(request.form['desired_percentage'])

        # Calculate the matching percentage for each resume
        matching_results = []

        for resume_path in resume_paths:
            matching_percentage = calculate_matching_percentage(job_description_path, resume_path)
            if matching_percentage is not None:
                matching_results.append((resume_path, matching_percentage))

        # Sort the matching_results list based on matching_percentage in descending order
        matching_results.sort(key=lambda x: x[1], reverse=True)

        # Delete the temporary files after processing
        os.remove(job_description_path)

        for resume_path in resume_paths:
            os.remove(resume_path)

        if matching_results:
            predictions = []
            for resume_path, matching_percentage in matching_results:
                prediction = f"Resume: {os.path.basename(resume_path)}, Matching Percentage: {matching_percentage:.2f}%"
                if matching_percentage >= desired_percentage:
                    prediction += " - Good Candidate"
                else:
                    prediction += " - Bad Candidate"
                predictions.append(prediction)
        else:
            predictions = ["Error: Unable to decode the files with the specified encodings."]
        return render_template('analyze.html', predictions=predictions)
    else:
        return render_template('analyze.html', prediction=None)


if __name__ == '__main__':
    # Ensure the "temp" directory exists for storing temporary files
    if not os.path.exists('files'):
        os.makedirs('files')
    app.run(port=3000, debug=True)