from fastapi import FastAPI
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
{
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
    },
    {
      "round_number": 3,
      "theme": "Задача по физике",
      "questions": [
        {
          "question": "Машина массой 1000 кг движется с ускорением 2 м/с². Какую силу нужно приложить, чтобы достичь такого ускорения?",
          "answer": "2000 Н",
          "explanation": "Используем второй закон Ньютона: F = m × a = 1000 кг × 2 м/с² = 2000 Н."
        }
      ]
    }
  ]
}
'''

@app.get("/")
async def main():
    try:
        response = ai_api.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=[{"role": "user", "content": f"Сгенерируй викторину в формате **JSON**, используя образец: {schema}. Отвечай только в формате JSON."}],
        )
        content = response.choices[0].message.content
        # Remove markdown code block markers if present
        if content.startswith("```json"):
            content = content[len("```json"):].strip()
        if content.endswith("```"):
            content = content[:-len("```")].strip()
        parsed = json.loads(content)
        return parsed
    except json.JSONDecodeError:
        return {"error": "Failed to parse AI response as JSON", "raw_response": content}
        # Remove markdown code block markers if present
