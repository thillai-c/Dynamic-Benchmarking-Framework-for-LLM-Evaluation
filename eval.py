import google.generativeai as genai

genai.configure(api_key="")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("What time did the sun rise in Salt Lake City on 2024-11-21? Give approximate value. Just give the value alone nothing else")
print(response.text)
