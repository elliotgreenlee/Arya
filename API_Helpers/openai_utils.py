from openai import OpenAI
from Utils.utils import load_json


class OpenAIAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def ask(self, model, prompt):
        openai_client = OpenAI(api_key=self.api_key)

        completion = openai_client.chat.completions.create(
            model=model,
            store=True,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return completion


def example():
    openai_credentials_path = '../Credentials/api_keys.json'
    api_keys = load_json(openai_credentials_path)
    openai = OpenAIAPI(api_keys['openai_api_key'])

    model = "gpt-4o"
    prompt = "write a haiku about ai"
    completion = openai.ask(model, prompt)

    print("=== Completion Details ===")
    print(f"Model: {completion.model}")
    print(f"Prompt: {prompt}")
    print("\n=== Response ===")
    print(completion.choices[0].message.content)
    print("\n=== Token Usage ===")
    print(f"Prompt Tokens: {completion.usage.prompt_tokens}")
    print(f"Completion Tokens: {completion.usage.completion_tokens}")
    print(f"Total Tokens: {completion.usage.total_tokens}")


if __name__ == '__main__':
    example()
