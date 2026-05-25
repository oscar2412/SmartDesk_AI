from dotenv import load_dotenv
import os

load_dotenv()

openai_key=os.getenv("OPENAI_API_KEY")
jira_email=os.getenv("JIRA_EMAIL")

print("OpenAI Key found:", openai_key is not None)
print("Jira Email found:", jira_email is not None)
