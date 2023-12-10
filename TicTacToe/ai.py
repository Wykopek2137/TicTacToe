from openai import OpenAI
from random import randint

class AI(OpenAI):
    def __init__(self, api_key=""):
        super().__init__(api_key=api_key)
    def process_response(self, **kwargs) -> int:
        
        prompt = f"Ty grasz {'znakiem X' if kwargs['side'] == 'x' else 'znakiem O'}. Przedstawie ci plansze idac kolumnami od samej gory. Plansza wyglada nastepujaca kolumna 1 =  1. {kwargs['positions'][0][1] if kwargs['positions'][0][0] else 'pusto'}, 2. {kwargs['positions'][1][1] if kwargs['positions'][1][0] else 'pusto'}, 3. {kwargs['positions'][2][1] if kwargs['positions'][2][0] else 'pusto'}, kolumna 2 = 4. {kwargs['positions'][3][1] if kwargs['positions'][3][0] else 'pusto'}, 5. {kwargs['positions'][4][1] if kwargs['positions'][4][0] else 'pusto'}, 6. {kwargs['positions'][5][1] if kwargs['positions'][5][0] else 'pusto'}, kolumna 3 = 7. {kwargs['positions'][6][1] if kwargs['positions'][6][0] else 'pusto'}, 8. {kwargs['positions'][7][1] if kwargs['positions'][7][0] else 'pusto'}, 9. {kwargs['positions'][8][1] if kwargs['positions'][8][0] else 'pusto'}. Wybierz gdzie chcesz sie poruszyc odpowiadajac tylko numerem pola. Poziom trudnosci wynosi {kwargs['hard_level']} z 4 dostepnych"
        self.stream = self.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Gramy w kolko i krzyzyk. Twoim zadaniem jest odpowiedzenie jedna cyfra bez tworzenia calego zdania gdzie chcesz sie poruszyc, czyli nie mowisz np Wybieram pole numer 4 tylko samo 4. Jesli podasz cos wiecej niz sam znak to spowodujesz blad w programie. Uzytkownik poda ci liste zajetych pol oraz jakim znakiem ty grasz. Dostaniesz takze informacje z jakim poziomem trudnosci masz dobierac swoje decyzje"},
            {"role": "user", "content": prompt}
            ],
        stream=True,
        )
        return self.protect_from_collision(self.receive_answer(), kwargs["positions"])
    
    def receive_answer(self) -> int:
        response = ""
        for chunk in self.stream:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
        return self.number_in_string(response)
    def number_in_string(self, response:str) -> int:
        for char in response:
            if char.isdigit():
                return int(char)
    def protect_from_collision(self, number:int, blocks:list) -> int:
        while blocks[number-1][0]:
            number = randint(1, 9)
        return number
    

