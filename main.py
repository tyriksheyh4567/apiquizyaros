from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from aiml_api import AIML_API
import json

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

schema = '''{
  "rounds": [
    {
      "round_number": 1,
      "theme": "Учёные: открытия, правила, законы",
      "questions": [
        {
          "question": "Кто сформулировал закон всемирного тяготения?",
          "options": [
            "Исаак Ньютон",
            "Галилео Галилей",
            "Альберт Эйнштейн",
            "Никола Тесла"
          ],
          "answer": "Исаак Ньютон",
          "explanation": "Исаак Ньютон сформулировал закон всемирного тяготения, который описывает силу притяжения между двумя массами."
        },
        {
          "question": "Какой учёный открыл закон электромагнетизма, связывающий электричество и магнитное поле?",
          "options": [
            "Джеймс Клерк Максвелл",
            "Майкл Фарадей",
            "Генрих Герц",
            "Анри Пуанкаре"
          ],
          "answer": "Майкл Фарадей",
          "explanation": "Майкл Фарадей открыл явление электромагнитной индукции, что является основой закона электромагнетизма."
        },
        {
          "question": "Кто сформулировал законы движения, известные как 'Законы Ньютона'?",
          "options": [
            "Исаак Ньютон",
            "Роберт Гук",
            "Джеймс Клерк Максвелл",
            "Нильс Бор"
          ],
          "answer": "Исаак Ньютон",
          "explanation": "Исаак Ньютон сформулировал три основных закона движения, которые лежат в основе классической механики."
        }
      ]
    },
    {
      "round_number": 2,
      "theme": "Формулы и физические величины",
      "questions": [
        {
          "question": "Какова формула для расчёта силы по второму закону Ньютона?",
          "options": [
            "F = m × a",
            "F = m / a",
            "F = a / m",
            "F = m + a"
          ],
          "answer": "F = m × a",
          "explanation": "Сила равна произведению массы тела на ускорение (F = m × a) согласно второму закону Ньютона."
        },
        {
          "question": "Какая физическая величина измеряется в Джоулях (Дж)?",
          "options": [
            "Работа",
            "Сила",
            "Масса",
            "Мощность"
          ],
          "answer": "Работа",
          "explanation": "Работа — это скалярная величина, измеряемая в Джоулях (Дж), показывающая количество энергии, переданное объекту."
        },
        {
          "question": "Какова формула для расчёта давления в жидкости?",
          "options": [
            "P = ρ × g × h",
            "P = m × a",
            "P = F / S",
            "P = v × t"
          ],
          "answer": "P = ρ × g × h",
          "explanation": "Давление в жидкости определяется формулой P = ρgh, где ρ — плотность жидкости, g — ускорение свободного падения, h — глубина."
        }
      ]
    }
  ]
}
'''

from fastapi import HTTPException

def fetch_ai_response(class_num: int):
    response = ai_api.chat.completions.create(
        model="gpt-4o-search-preview",
        web_search_options={},
        messages=[{
            "role": "user",
            "content": f"Напиши задачи по физике на **{class_num}** классе в формате **JSON**, используя образец: {schema}. 1-ый и 2-ой раунд - по 3 вопроса на каждый, 3 раунд - одна задача по физике. 1-ый раунд: учёные, правила, законы; 2-ой раунд - формулы, величины. Вывод только в JSON. Ищи реальные примеры в интернете."
        }]
    )
    text = response.choices[0].message.content

    if text.startswith("```json"):
        text = text[len("```json"):].strip()
    if text.endswith("```"):
        text = text[:-3].strip()
    try:
        json_data = json.loads(text)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON response from AI")

    return json_data

@app.get("/")
async def main(class_num: int = Query(None, ge=7, le=11)):
    if class_num is None:
        raise HTTPException(status_code=400, detail="Missing required query parameter: class_num")
    json_response = fetch_ai_response(class_num)
    return json_response
