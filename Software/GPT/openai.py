from openai import OpenAI

client = OpenAI(
api_key = "<your_llamaapi_token>",
base_url = "https://api.llama-api.com"
)

response = client.chat.completions.create(
model="llama3.1-70b",
messages=[
    {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
    {"role": "user", "content": "Who were the founders of Microsoft?"}
],


)

#print(response)
print(response.model_dump_json(indent=2))
print(response.choices[0].message.content)