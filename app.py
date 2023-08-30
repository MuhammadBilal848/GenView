from flask import Flask , redirect , url_for , render_template,request,jsonify
import json
from questions import gpt_qs
from response_read import generated_qs , speak_qs , correct_or_not , clear_text_file , sophisticated_response , get_answer_from_gpt
from qdrant.qdrant_module import upload_embd_get_similarity
import time
import random

app = Flask(__name__)

  
@app.route('/api/submit-details', methods=['POST', 'GET'])
def submitDetails():
    if request.method == 'POST':
        try:
            clear_text_file('questions.txt')
            data = request.get_json()  # Parse JSON data from request body
            name = data['name']
            father_name = data['father_name']
            age = int(data['age'])
            university = data['university']
            prior_experience = int(data['prior_experience'])
            skills = data.get('skill_and_experience', [])  # Use a default empty list if 'skill' is missing
            response_data = {
                "name": name,
                "father_name": father_name,
                "age": age,
                "university": university,
                "prior_experience": prior_experience,
                "skill_and_experience": skills}
            final_dic = {'user_details': response_data}
            s_e = response_data['skill_and_experience']
            for i in s_e:
                skill, experience = i.split(',')
                gpt_qs(skill, experience)
            question_list = generated_qs()
            final_dic['questions'] = question_list
            return jsonify(final_dic)
        except Exception as e:
            return jsonify(error=str(e)), 400
    else:
        return "This route only accepts POST requests."


@app.route('/api/evaluate-answers', methods=['POST'])
def evaluateAnswers():
    try:
        data = request.get_json()  # Parse JSON data from request body

        if not isinstance(data, list):
            return jsonify(error="Invalid JSON data, expected a list"), 400
        evaluation_responses = []

        for question_data in data:
            question = question_data.get('question')
            answer = question_data.get('user_answer')
            if question and answer:
                evaluation_responses.append(upload_embd_get_similarity(answer , get_answer_from_gpt(question).replace('\n', ''))*100)
            else:
                evaluation_responses.append({'error': 'Missing question or answer'})
        sop_res = sophisticated_response(evaluation_responses)
        return jsonify(sop_res)
    except Exception as e:
        return jsonify(error=str(e)), 500

# @app.route('/')
# def home():
#     return render_template('index.html')


# @app.route('/submit',methods = ['POST','GET'])
# def submit():
#     if request.method == 'POST':
#         name = request.form['name']
#         father_name = request.form['fatherName']
#         age = int(request.form['age'])
#         university = request.form['university']
#         prior_experience = int(request.form['priorExperience'])
#         skills = request.form.getlist('skill[]')

#         response_data = {
#             "name": name,
#             "father_name": father_name,
#             "age": age,
#             "university": university,
#             "prior_experience": prior_experience,
#             "skill & experience": skills    }

#         final_dic = {
#             'user_details':response_data
#         }
#         s_e = response_data['skill & experience']
#         random.shuffle(s_e)
#         for i in s_e:
#             skill , experience = i.split(',')
#             gpt_qs(skill,experience)

#         question_list = generated_qs()
        
#         final_dic['questions'] = question_list
        
#     return jsonify(final_dic)


# @app.route('/interview/')
# def interview():
#     question_list = generated_qs()

#     return render_template('interview.html', question_list=question_list)


# list_of_dic_Qs_userAns = []
# @app.route('/submit_answer', methods=['POST'])
# def submit_answer():
#     q_a = {}
#     if request.method == 'POST':
#         data = request.json
#         question = data.get('question')
#         user_answer = data.get('userAnswer')
#         q_a['question'] = question
#         q_a['user_answer'] = user_answer
#         list_of_dic_Qs_userAns.append(q_a)
#         message = {"Message": "Answer received successfully"}
#         return jsonify(message)  # Return a JSON response
#     else:
#         return '', 204  # Return a No Content response


# @app.route('/all_qs_ans', methods=['GET'])
# def all_qs_ans():
#     return jsonify(list_of_dic_Qs_userAns)


# list_of_dic_Qs_gptAns = []
# similarity_result = []
# @app.route('/finaljson', methods=['GET'])
# def finaljson():
#     dic = generated_qs()
#     for i in dic:
#         new_a = {}
#         new_a['question'] = i
#         new_a['gpt_answer'] = get_answer_from_gpt(i).replace('\n', '')
#         list_of_dic_Qs_gptAns.append(new_a) 
#     for a in range(len(list_of_dic_Qs_gptAns)):
#         similarity = {}
#         similarity[f'Answer {a}']  = upload_embd_get_similarity(list_of_dic_Qs_userAns[a]['user_answer'],list_of_dic_Qs_gptAns[a]['gpt_answer'])
#         similarity_result.append(similarity)
#     return jsonify(similarity_result)

# @app.route('/evaluate', methods=['GET'])
# def evaluate():
#     evaluation_responses = []
#     dic = list_of_dic_Qs_userAns
#     for i in dic:
#         evaluation_responses.append(correct_or_not(i['question'],i['user_answer']).replace('\n', ''))
#     sop_res = sophisticated_response(evaluation_responses)
#     return jsonify(sop_res)



if __name__ == '__main__':
    app.run(debug=True)




# list_of_dic_Qs_gptAns = []
# @app.route('/finaljson', methods=['GET'])
# def finaljson():
#     dic = generated_qs()
#     for i in dic:
#         new_a = {}
#         new_a['question'] = i
#         new_a['gpt_answer'] = get_answer_from_gpt(i).replace('\n', '')
#         list_of_dic_Qs_gptAns.append(new_a) 
#     return jsonify(list_of_dic_Qs_gptAns)


# similarity_result = []
# @app.route("/compare", methods=["GET"])
# def compare():
#     for a in range(len(list_of_dic_Qs_gptAns)):
#         similarity = {}
#         similarity[f'Answer {a}']  = upload_embd_get_similarity(list_of_dic_Qs_userAns[a]['user_answer'],list_of_dic_Qs_gptAns[a]['gpt_answer'])
#         similarity_result.append(similarity)
#     return jsonify(similarity_result)
s