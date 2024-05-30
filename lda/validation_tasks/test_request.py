from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = ""
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant evaluating the top words of a topic model output for a given topic. Please provide a category in German describing the following keywords. Reply with one or two words."},
    {"role": "user", "content": "'Unfall', 'fahren', 'Uhr', 'Fahrzeug', 'verletzen', 'Fahrer', 'Spital', 'Polizei', 'Kantonspolizei', 'Strasse'"}
  ]
)

print(completion.choices[0].message)