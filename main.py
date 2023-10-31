import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as json_file:
            knowledge_base = json.load(json_file)
            if "questions" not in knowledge_base:
                print("ไม่พบข้อมูล 'questions' ในไฟล์ที่กำหนด")
                return {}
            return knowledge_base
    except FileNotFoundError:
        print(f"ไฟล์ '{file_path}' ไม่พบ")
        return {}
    except json.JSONDecodeError:
        print(f"เกิดข้อผิดพลาดในการอ่าน JSON จาก '{file_path}'")
        return {}

def save_knowledge_base(file_path: str, knowledge_base: dict):
    try:
        with open(file_path, 'w') as json_file:
            json.dump(knowledge_base, json_file, indent=2)
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการบันทึก JSON ไปยัง '{file_path}': {e}")

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

def chat_bot():
    knowledge_base = load_knowledge_base('knowledge_base.json')

    while True:
        user_input = input('You: ')

        if user_input.lower() == 'quit':
            break

        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer = input('Type the answer or "skip" to skip: ')
            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank you! I learned a new response!')

if __name__ == '__main__':
    chat_bot()
