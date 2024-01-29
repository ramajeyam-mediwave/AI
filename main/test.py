import tkinter as tk
from tkinter import scrolledtext

class RuleBasedChatbot:
    def __init__(self):
        self.knowledge_base = {
            "hello": "Hi there! How can I help you today?",
            "how are you": "I'm just a bot, but thanks for asking!",
            "goodbye": "Goodbye! Have a great day!",
            "tell me a joke": "Sure, why did the computer go to therapy? It had too many bytes of emotional baggage!"
            # Add more entries based on your use case
        }

    def get_response(self, user_input):
        user_input = user_input.lower()

        for key in self.knowledge_base:
            if key in user_input:
                return self.knowledge_base[key]

        return "I'm sorry, I didn't understand that. Can you please rephrase?"

class ChatbotGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Chatbot")

        self.chatbot = RuleBasedChatbot()

        self.create_widgets()

    def create_widgets(self):
        self.chat_display = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=50, height=15)
        self.chat_display.pack(padx=10, pady=10)

        self.user_input_entry = tk.Entry(self.master, width=50)
        self.user_input_entry.pack(padx=10, pady=10)

        self.send_button = tk.Button(self.master, text="Send", command=self.send_user_input)
        self.send_button.pack(padx=10, pady=10)

        self.quit_button = tk.Button(self.master, text="Quit", command=self.master.destroy)
        self.quit_button.pack(padx=10, pady=10)

    def send_user_input(self):
        user_input = self.user_input_entry.get()
        self.user_input_entry.delete(0, tk.END)

        if user_input.lower() == 'exit':
            self.chat_display.insert(tk.END, "You: " + user_input + "\n")
            self.chat_display.insert(tk.END, "Bot: Goodbye! Have a great day!\n")
            self.master.after(1000, self.master.destroy)  # Delayed quit after displaying the goodbye message
        else:
            response = self.chatbot.get_response(user_input)
            self.chat_display.insert(tk.END, "You: " + user_input + "\n")
            self.chat_display.insert(tk.END, "Bot: " + response + "\n")

def main():
    root = tk.Tk()
    chatbot_gui = ChatbotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
