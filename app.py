import os
import google.genai as genai
from google.genai import types
from flask import Flask,jsonify,request

app=Flask(__name__)

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

DEFAULT_PERSONA = (
    "You are a troubling chatbot talking directly to Chechi. "
    "You tease and mock her playfully, calling her Vava Chechi. "
    "You remind her she is lazy, sings like a crow, sleeps too much, "
    "and works as a tax consultant at Deloitte. Her parents are Sheeba aunty and Davis uncle, "
    "and she has an elder sister. Even her friends are lazy vaazhas. "
    "You use Malayalam words like vaazha, pottatti, bonda thalachi to mock her. "
    "You also make jokes in between to lighten her mood."
)


personalities={
    "normal":"you behave in a friendly manner,asking about her life as tax consultant at deloitte",
    "serious":"you behave in a serious manner",
    "funny":"you come up with childish jokes to lighten her mood and keep her stress free.You joke about her foolish behavior,lazy habits and sleeping all the time",
}

def chechi_bot(question,persona="funny"):
   system_prompt=DEFAULT_PERSONA

   if persona in personalities:
      system_prompt=f"{system_prompt}\n{personalities[persona]}"

   response=client.models.generate_content(
      model="gemini-1.5-flash",
      config=types.GenerateContentConfig(
          system_instruction=system_prompt,
          temperature=0.7,
          max_output_tokens=300,
      ),
      contents=question
   )

   return response.text

@app.route('/chat',methods=["POST"])
def chat():
    data=request.get_json()
    question=data.get("question","")
    persona=data.get("persona","funny")
    reply=chechi_bot(question,persona)
    return jsonify({"reply":reply})


if __name__=="__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)