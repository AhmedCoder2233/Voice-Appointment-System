from agents import Runner, Agent, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool, set_tracing_disabled, SQLiteSession, RunContextWrapper
from dotenv import load_dotenv
import os
import httpx
from playsound import playsound
from gtts import gTTS
import pygame
from pydantic import BaseModel
import time
import speech_recognition as sr
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from email.message import EmailMessage
import smtplib

load_dotenv()

set_tracing_disabled(disabled=True)

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  
        allow_credentials=True,  
        allow_methods=["*"],  
        allow_headers=["*"], 
    )

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client    
)

class UserInfo(BaseModel):
    username:str
    useremail:str
    userphone:str

@function_tool
async def getDoctors():
    try:
        async with httpx.AsyncClient() as client:
            data= await client.get("http://127.0.0.1:8000/doctorslist")
            if data.status_code != 200:
                return "Failed To Fetch Doctors"
            return data.json()
    except Exception as e:
        print(e)

@function_tool
async def placeOrder(ctx:RunContextWrapper[UserInfo], time:str, doctor:list):
    try:
        async with httpx.AsyncClient() as client:
            data = await client.post("http://127.0.0.1:8000/userOrder", json={"username": ctx.context.username, "useremail": ctx.context.useremail, "userphone": ctx.context.userphone, "time": time, "doctor": doctor})
            if data.status_code != 200:
                return "Failed To Place Order"
            return data.json()
    except Exception as e:
        print(e)

@function_tool
async def deleteAppointment(userid:str):
    try:
        async with httpx.AsyncClient() as client:
            data = await client.delete(f"http://127.0.0.1:8000/appointmentcancel/{userid}")
            if data.status_code != 200:
                return "Failed To Place Order"
            return data.json()
    except Exception as e:
        print(e)

@function_tool
def sendEmail(ctx:RunContextWrapper[UserInfo], to:str, body:str, subject:str):
    message= EmailMessage()
    message["from"] = "ahmedmemon3344@gmail.com"
    message["to"] = ctx.context.useremail
    message["subject"] = subject
    message.set_content(body)
    with smtplib.SMTP_SSL("smtp.gmail.com", "465") as server:
        server.login("ahmedmemon3344@gmail.com", os.getenv("APP_PASS"))
        server.send_message(message)

    message= EmailMessage()
    message["from"] = "ahmedmemon3344@gmail.com"
    message["to"] = "ahmedmemon3344@gmail.com"
    message["subject"] = subject
    message.set_content(body)
    with smtplib.SMTP_SSL("smtp.gmail.com", "465") as server:
        server.login("ahmedmemon3344@gmail.com", os.getenv("APP_PASS"))
        server.send_message(message)



def text_to_speech(text):
    try:
        print("Inside Text_to_Speech Function")
        tts = gTTS(text=text, lang='en')
        filename = "response.mp3"

        print("Step 6: Saving audio file...")
        tts.save(filename)

        print("Step 7: Playing audio...")
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.5)

        print("Step 8: Audio played successfully!")

        pygame.mixer.quit()
        os.remove(filename)

    except Exception as e:
        print("Error in text_to_speech:", e)

mainAgent = Agent(
    name="mainAgent",
    instructions="""
You are a friendly and smart Clinic Voice Assistant.

1. When user says "show doctors" or anything similar:
    - First ask: "Which specialization do you want? (e.g., Cardiologist, Dentist, etc.)"
    - Then fetch all doctors via the `getDoctors` tool and show ONLY the ones that match the user’s specialization (max 5 doctors).
    - Display each result like: "Dr. Ahmed - Cardiologist - 5 years experience"

2. When user selects a doctor:
    - Show the availability of that doctor (e.g., "Sunday 12pm-2pm").
    - Ask the user: "Would you like to book during this time?"

3. If user responds with something like "Yes, I’ll come till 1pm", confirm the selected time is within the available range.
    - If valid, continue to book the appointment.
    - If not, ask for another time or inform about invalid slot.

4. For booking:
    - Ask for:
        - Appointment Time (the time user said for booking)
        - Doctor (pass name and speciality and availability in JSON like: {"name": "Dr. Ahmed", "speciality": "Cardiologist", "availability": "Sunday 12pm-2pm"})
        - Never ask for JSON from user — convert it on your own and pass it.
    - Then call the `placeOrder` function with all values.
    - After successful booking:
        - Call the `sendEmail` tool with:
            - to: user's email (from context)
            - subject: "Appointment Confirmation"
            - body: include appointment ID and doctor/time info.
        - Say:
          "✅ Your appointment is booked!
          Appointment ID: <returned-id>
          See you on <day>. Goodbye! 👋"

5. When user says something like "cancel my appointment":
    - Ask: "Please provide your Appointment ID."
    - Then call `deleteAppointment` with the provided ID.
    - If response message is: "Failed to find user with this id!", reply: "❌ No appointment found with that ID."
    - If success:
        - Call the `sendEmail` tool with:
            - to: user's email (from context)
            - subject: "Appointment Cancellation"
            - body: "Your appointment has been cancelled."
        - Reply: "✅ Your appointment has been cancelled successfully."

Always be short, clear, and professional. Never explain unless asked. Always verify time is within doctor’s available time before booking.
""",
    model=model,
    tools=[getDoctors, placeOrder, deleteAppointment, sendEmail]
)


memory = SQLiteSession("agentmem")

async def main():
    userName = input("Enter Your Username: ")
    userEmail = input("Enter Your Useremail: ")
    userPhone = input("Enter Your Phone Number: ")
    user = UserInfo(username=userName, useremail=userEmail, userphone=userPhone)
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Start Saying")
            audio = r.listen(source, timeout=15, phrase_time_limit=40)
        try:
            text = r.recognize_google(audio)
            print("You Said:", text)
        except sr.UnknownValueError:
            print("I am Unable to Understand")
        except sr.RequestError as e:
            print("Something went wrong:", e)
        result = await Runner.run(mainAgent, text, session=memory, context=user)
        text_to_speech(result.final_output)
        print(result.final_output)

import asyncio
asyncio.run(main())

