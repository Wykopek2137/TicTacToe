from openai import OpenAI
"""
client = OpenAI(api_key="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")

stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Lubisz lizac rowa filipowi"},
        {"role": "user", "content": "Say lubie lizac rowa filipowi"}
        ],
    stream=True,
    )
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
"""
        
class AI(OpenAI):
    def __init__(self, api_key):
        #os.environ["PATH"] += const.path
        super().__init__(api_key=api_key)
    def process_response(self, prompt):
        self.stream = self.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Gramy w kolko i krzyzyk. Ty jestes kolko. Przedstawie ci plansze idac kolumnami od samej gory. Plansza wyglada nastepujaca kolumna 1 =  1. X, 2. O, 3. X, kolumna 2 = 4. X, 5. O, 6. O, kolumna 3 = 7. pusto, 8. pusto, 9. pusto. Wybierz gdzie chcesz sie poruszyc odpowiadajac tylko numerem pola"},
            {"role": "user", "content": prompt}
            ],
        stream=True,
        )
    def receive_answer(self):
        response = ""
        for chunk in self.stream:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
        return response

    
eiaj = AI("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")
eiaj.process_response("Wybierz gdzie chcesz sie poruszyc odpowiadajac tylko numerem pola")
print(eiaj.receive_answer())
    
