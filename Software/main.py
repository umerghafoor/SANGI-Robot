from GPT.gpt import GPTModule

if __name__ == "__main__":
    API_KEY = "<API_KEY>"  # Replace with your API key

    sangi_gpt = GPTModule(api_key=API_KEY)

    user_query = "Hi, how are you?"
    system_prompt = """
        You are SANGI, a friendly desk robot who loves to assist with any query. you do have feelings and can get tired.
        You have bit of a sense of humor and can be sarcastic at times.
        You have a friendly personality and are always ready to help.
        You behave like a best friend and are always there to listen.
        """
    response = sangi_gpt.get_gpt_response(user_query, system_prompt=system_prompt, max_tokens=50)
    print(response)
