from fastapi import FastAPI
from pydantic import BaseModel
from search import run_command
class Input(BaseModel):
    search_keyword: str

app =  FastAPI()

@app.post("/socialmedia", status_code=200, description="Search for all possible social media accounts related to the keyword")
def search_by_name(input: Input):
    command = f'python spiderfoot/sf.py -m sfp_accounts -s "{input.search_keyword}"  -q -o json'
    results = run_command(command)
    return results

@app.post("/aiprompt",status_code=200,description='prompt ai')
async def prompt_ai(input: Prompt):
    response = await prompt_deepseek(input.prompt + ' ')
    return response



    
    
