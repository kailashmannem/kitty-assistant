# 🐾 Kitty Assistant — Your Desktop AI Cat Companion
🎮 Platform: Windows Desktop App (built with PyQt5 + Pygame) <br>
💬 Features: Animated cat sprite, local AI integration, Chat-box interactions

Kitty Assistant is a cute, pixel-style AI cat that lives on your desktop. It roams around, performs little actions, and even talks back in a cattish voice — making productivity and daily tasks just a bit more fun.

# 💡 Motivation
Most AI assistants are either boring or overly formal.

I wanted to build something playful, interactive, and personal — a desktop companion.

Kitty Assistant brings that idea to life:

- A sprite-animated cat that idles, walks, jumps, and sleeps on your desktop
- Gives you responses with a fun “cattish” voice filter
- Doubles as a floating pet to keep your desktop alive!
- Whether you’re working, studying, or just vibing — Kitty is always by your side.

# 🌀 Project Workflow
Here's how the Kitty Assistant works under the hood:

- Launch the App: <br>
A PyQt5-based transparent window spawns an animated cat on your screen. (Asks for Gemini API key for the first time)

- Sprite Animation: <br>
The cat uses Pygame-powered sprite sheets (Idle, Walk, Jump, Sleep, Dance) to animate fluidly.

- Chat Box Trigger (Single-Click): <br>
A single click on Kitty enables chat mode. You can chat with kitty!

- AI Reply Generation: <br>
The query is sent to your respective Gemini API, which generates a smart, context-aware response.

- Random Wandering: <br>
When idle, Kitty moves around the screen, sleeps, or reacts to mouse movement.

# 🛠️ Tech Stack
## ⚙️ Core Libraries
- PyQt5 – Transparent, borderless desktop app window
- Pygame – Sprite-based animation for idle, walk, jump, sleep, etc.
- Gemini API – Processes your query and generates the AI response
- pyinstaller – For packaging and distributing as an installer

## 🧪 Features
✅ Single-click to talk with Kitty

✅ Sprite-based animations: idle, walk, jump, sleep, dance

✅ AI-powered response system (Gemini)

✅ Sleep and wake-up behavior based on mouse interaction

✅ Portable desktop experience with no setup required

## 📦 Installation & Deployment
- We use PyInstaller to bundle all dependencies into a standalone .exe.

### For End Users
- Download the installer .exe file from the Releases tab.

- Run the installer (one-time).

- A shortcut will be added to your desktop — click it to launch Kitty.

- Enter your Gemini API key, as it is mandatory for the app to continue.
  
- Kitty will start floating on your screen with all necessary files pre-downloaded.

- No need to install Python, pip, or any other tools.

# ⚠️ Security Notice
This app is unsigned, so Windows might show a "protected your PC" warning. This is expected for apps not published by large vendors.

💡 To verify the safety of the app:

- You can view or audit the full source code here: GitHub Repo

- This installer was built directly from this open-source code using auto-py-to-exe

- Requires internet access only for chatbox as it requires receiving and sending tokens across internet to your Gemini API.

- Also note that the application requires a Gemini API key as of now to function, I personally don't take or use your key. It is saved inside the application files so that it doesn't prompts multiple times for the key and directly pulls the key from the gemini_api_key.txt file.

✅ Click "More Info" → "Run Anyway" to proceed if you trust the app.

# 🧙‍♂️ Future Additions
- Voice Integration

- Multiple voice models (choose your cat!)

- Drag-and-drop mini games

- Discord/Spotify/Notion integration

# 🤝 Contributions & Issues
Want to improve Kitty? Add new animations or voice effects? Stuck and not understand how to work around? Here's how:
- Raise a issue or connect with me on linkedin!
