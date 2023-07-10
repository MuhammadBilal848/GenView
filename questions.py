import os
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain


os.environ['OPENAI_API_KEY'] = openai_key
llm = OpenAI(temperature=0.8)


first_question = PromptTemplate(
    input_variables = ['skill_qs','experience'] ,
    template = 'Write 2 difficult questions about {skill_qs} skill for a person having {experience} years of experience')

# tempratture param controls how balance the reponse should be
question = LLMChain(llm=llm , prompt=first_question,verbose=True) 

sk_exp = [('pandas',1),('tensorflow',3),('flask',2),('react.js',3),('Opencv',5),('Sequence Models',2),('Dockers',5)]
for skill,experience in sk_exp:
    response = question.run(skill_qs=skill, experience=experience)
    with open('questions.txt', 'a') as file:
        file.write(response)