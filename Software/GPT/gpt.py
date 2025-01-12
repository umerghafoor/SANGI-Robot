from openai import OpenAI

class GPTModule:
    def __init__(self, api_key, base_url="https://openrouter.ai/api/v1", model="openai/gpt-3.5-turbo"):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        self.model = model

    def get_gpt_response(self, user_input, referer=None, title=None, system_prompt=None, max_tokens=None):
        try:
            extra_headers = {}
            if referer:
                extra_headers["HTTP-Referer"] = referer
            if title:
                extra_headers["X-Title"] = title

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": user_input})

            completion = self.client.chat.completions.create(
                extra_headers=extra_headers,
                model=self.model,
                messages=messages,
                max_tokens=max_tokens
            )

            return completion.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

