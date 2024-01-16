import os
import openai

# Khai báo API key
openai.api_key = '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'

messages = [ {"role": "system", "content":  

              "You are a intelligent assistant."} ] 
def openai_chat():
    while True:
        message = input("User: ")

        if message.lower() == "exit":
            print("Exiting the program...")
            break

        if message:
            messages.append(
                {"role": "user", "content": message},
            )

            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )

            reply = chat.choices[0].message.content
            print(f"ChatGPT: {reply}")
            print("*ChatGPT can make mistakes. Consider checking important information.")
            print("*Type 'exit' to exit the program.")
            messages.append({"role": "assistant", "content": reply})
