!pip install -q -U google-genai
from google import genai
from google.genai import types
from google.colab import userdata

api_key = userdata.get('GOOGLE_API_KEY')
client = genai.Client(api_key=api_key)

def get_history(name: str) -> str:
    """TOOL 1: Patient history"""
    return f"{name}: Last visit 12 Aug, fever, given Panadol. 2 visits before."

def calculator(expr: str) -> str:
    """TOOL 2: Calculator - SAFE"""
    try:
        allowed = "0123456789*+-/(). "
        if not all(c in allowed for c in expr):
            return "Invalid chars"
        return str(eval(expr))
    except Exception as e:
        return f"Error: {e}"

# USE MODEL FROM YOUR LIST - NOT 3.6-flash
response = client.models.generate_content(
    model="gemma-4-26b-a4b-it",  # <- This is IN your available list, stable
    contents="Ahmed ko bukhar hai, history dekho aur 500*2 calculate karo",
    config=types.GenerateContentConfig(
        tools=[get_history, calculator],
        system_instruction="You are clinic receptionist in Larkana. Check history first, answer in short Urdu, add 'Doctor se consult karo' at end.",
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False)
    )
)

print(response.text)
