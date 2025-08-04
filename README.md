# 🎙️ Voice-Based Appointment Booking System

This project lets users **book or cancel doctor appointments** using their **voice only** — no clicks or forms required. AI listens to the user, understands the request, and responds in real-time with voice. 💬🔁

---

## 🚀 Features

- 🔊 **Voice-Controlled Interaction**  
  Speak naturally to book or cancel an appointment — fully hands-free.

- 🧠 **AI Understanding (Gemini + OpenAI)**  
  Understands context like:
  - “Book an appointment with Dr. Ali tomorrow at 5 PM”
  - “Cancel my appointment — ID 7626”

- 🗣️ **Real-Time Voice Replies**  
  System talks back using `gTTS` — no typing needed.

- 🗃️ **Database-Backed**  
  Appointments are saved in **PostgreSQL**

- 📧 **Email Confirmation**  
  Appointment details sent via SMTP email

---

## 🛠️ Tech Stack

| Layer        | Technology Used                  |
|--------------|----------------------------------|
| 🧠 AI Models | OpenAI SDK, Gemini API           |
| 🗣️ Voice     | SpeechRecognition, gTTS          |
| ⚙️ Backend   | FastAPI                          |
| 🧵 Database  | PostgreSQL                       |
| 📧 Email     | SMTP (Secure Mail)               |

---

## 🎯 How It Works

1. **User speaks** a sentence like:
   - _“Book an appointment with Dr. Usman tomorrow at 4 PM.”_
   - _“Cancel my appointment. Order ID 7626.”_

2. **SpeechRecognition** converts it to text.

3. **AI Agent** (via Gemini + OpenAI SDK) understands intent.

4. - If it’s a booking: Details are saved to PostgreSQL & confirmation is sent.
   - If it’s a cancellation: Appointment is removed by ID.

5. **System responds** with a voice message using `gTTS`.
