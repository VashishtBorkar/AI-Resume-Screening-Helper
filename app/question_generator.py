import openai
import os
import re
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env into the environment
openai.api_key = os.getenv("OPENAI_API_KEY")


def load_prompt(file_path, skills):
    with open(file_path, 'r', encoding='utf-8') as f:
        template = f.read()
    return template.replace("{{skills}}", ", ".join(skills))

def parse_questions_and_answers(raw_output):
    pattern = r"Question:\s*(.*?)\n\s*Answer:\s*(.*?)(?=\n\s*Question:|\Z)"
    matches = re.findall(pattern, raw_output, re.DOTALL)
    return [{"question": q.strip(), "answer": a.strip()} for q, a in matches]

def generate_questions(skills, prompt_path='../prompts/screening_prompt.txt', dev=False):
    if dev:
        raw_output = """
                    Question: How would you structure an Express.js application to support scalability and maintainability in a production-grade REST API?
                    Answer: A well-structured Express.js app uses a modular architecture with separate folders for routes, controllers, services, and middleware, and follows patterns like MVC; tools like environment-based configs, error handlers, and logging enhance maintainability and scalability.
                    
                    Question: If a Node.js server is experiencing performance bottlenecks under high load, how would you diagnose and resolve the issue?
                    Answer: Diagnosing performance issues in Node.js involves profiling the event loop with tools like clinic.js or node --inspect, analyzing asynchronous operations, and using clustering or load balancers to handle CPU-bound tasks and scale across multiple processes.
                    """
    else:
        prompt = load_prompt(prompt_path, skills)
        print(prompt)

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        raw_output = response['choices'][0]['message']['content']

    return parse_questions_and_answers(raw_output)
