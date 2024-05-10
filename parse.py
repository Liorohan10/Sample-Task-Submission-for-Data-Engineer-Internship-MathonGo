import re
import json

def create_json_from_txt(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    questions = content.split('Question ID: ')[1:]
    data = []

    for i, question in enumerate(questions):
        question_id, question_text = question.split('\n', 1)
        question_id = re.sub(r'\D', '', question_id)
        if '\\section*{Answer (' in question_text:
            question_text, answer_section = question_text.split('\\section*{Answer (', 1)
            answer, solution = answer_section.split(')}', 1)
            question_text = re.sub(r'(?<!\\)\\(?!\\)', '\\\\\\\\', question_text.strip())
            question_text = re.sub('\n+', '\n', question_text)
            solution = re.sub(r'(?<!\\)\\(?!\\)', '\\\\\\\\', solution.strip()).replace('Sol. ', '')

            split_text = re.split('\(A\)|\(B\)|\(C\)|\(D\)', question_text)
            question_text = split_text[0].strip()
            options_text = split_text[1:]
            options = [{'optionNumber': j+1, 'optionText': option.strip().replace('\\', '\\\\'), 'isCorrect': chr(65+j) == answer} for j, option in enumerate(options_text) if option]

            data.append({
                'questionNumber': i+1,
                'questionId': int(question_id),
                'questionText': question_text,
                'options': options,
                'solutionText': solution
            })

    with open('output.json', 'w') as f: #The output will be stored in this JSON file
        json.dump(data, f, indent=4)

create_json_from_txt('Task.txt') #Replace Task.txt with the text file you want to parse





















