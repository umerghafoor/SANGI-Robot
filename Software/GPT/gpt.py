import json
from llamaapi import LlamaAPI

class LlamaGPTModule:
    def __init__(self, api_token, model="llama3.3-70b"):
        """
        Initialize the LlamaGPTModule with API token and model.

        Parameters:
            api_token (str): Your Llama API token.
            model (str): The model to use for generating responses.
        """
        self.llama = LlamaAPI(api_token)
        self.model = model

    def generate_response(self, user_input):
        """
        Generate a response using the Llama API based on user input.

        Parameters:
            user_input (str): The user's input query.

        Returns:
            str: The generated response or error message.
        """
        # Build the API request
        api_request_json = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": user_input},
            ],
            "functions": [
                {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g., San Francisco, CA",
                            },
                            "days": {
                                "type": "number",
                                "description": "Number of days ahead for the forecast",
                            },
                            "unit": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"],
                                "description": "Temperature unit",
                            },
                        },
                        "required": ["location", "days"],
                    },
                }
            ],
            "stream": False,
            
        }

        try:
            # Execute the API request
            response = self.llama.run(api_request_json)
            return json.dumps(response.json(), indent=2)  # Pretty-print the JSON response
        except Exception as e:
            return f"Error generating response: {e}"


# Example Integration with Robot Input/Output
if __name__ == "__main__":
    # Replace with your actual API token
    api_token = "LA-46a713b10ae6424ab072b0a9234ebf4754e35fae4c2a445ab914b3f5eba45817"

    gpt_module = LlamaGPTModule(api_token)

    print("Llama GPT Module Initialized. Type 'exit' to quit.")
    try:
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Exiting Llama GPT module.")
                break

            response = gpt_module.generate_response(user_input)
            print(f"Robot: {response}")
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt detected. Exiting Llama GPT module.")
