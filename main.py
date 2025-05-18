from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from aiml_api import AIML_API

ai_api = AIML_API()

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

response = ai_api.chat.completions.create(
    model="gpt-4o-search-preview", 
    messages=[
        {
            "role": "user", 
            "content": "Напиши квиз на **русском языке** в формате JSON. В ответе пиши **только** JSON. Тема - физика. Всего 3 раунда, в 1-ом и во 2-ом раунде - по 3 вопроса. Первый раунд - вопросы про учёных: открытия, правила, законы. 2-ой раунд - различные формулы, величины. 3-ий раунд - одна задача по физике. Для каждого вопроса и последней задачи делай объяснение (значение в JSON). _Ключи_ на **английском**, _значения_ на **русском**."
        }
    ]
)
prefinal_response = response.choices[0].message.content.replace("`", "")
prefinal_response = prefinal_response.replace("json","")
final_response = jsonable_encoder(prefinal_response)

@app.get("/")
async def main():
    return final_response