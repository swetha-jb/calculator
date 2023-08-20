"""
File: solver_ai.py
Description:
    Implements an ai solver using the OpenAI API for
    the word problem page in main.py.
"""

import os
from dotenv import load_dotenv
import openai


# Set API key
load_dotenv('.env')
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate(problem):
    """
    Generates a response from chat AI based on user input problem

    :param problem: string of problem
    :returns: generated response
    """

    prompt = f'Solve the following problem: {problem}. Make sure your answer is easily readable'

    # Generate response to prompt
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = [
            {'role': 'user', 
            'content': prompt }
        ]
    )
    
    answer = response.choices[0].message.content
    return answer


# Test:
if __name__ == '__main__':
    prob = 'Jared has 10 donuts and Michael has 24 donuts. How many more donuts does Michael have than Jared?'
    ans = generate(prob)
    print(ans)