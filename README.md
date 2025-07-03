# 🎯 Quiz Builder | AI-Based Quiz Generator

Quiz Builder is a web-based application designed for developers to generate tailored quiz questions based on specific skill sets, experience levels, and topic scopes using AI. It utilizes local large language models (LLMs) for fast and private quiz generation.

![Demo of the Quiz App](https://github.com/Vishal-Patoliya/quiz_builder/blob/main/QuizBuilder.gif)

---

## 🧠 Features

- 🔍 Generate quiz questions based on selected skills and expertise.
- 🧑‍💻 Choose difficulty levels and topic scope.
- 🤖 Powered by local AI models using [Ollama](https://ollama.com/).
- 🚀 Supports integration with **Strands Agent** from AWS AI for enhanced question generation and personalization.
- ⚡ Fast response with Mistral (lightweight LLM).
- 🌐 Built with Streamlit for an interactive frontend.
- 🛠 Developer-friendly setup using `pipenv`.

---

## 🚀 Getting Started

### 1. Clone the Repository

```
git clone https://github.com/Vishal-Patoliya/quiz_builder.git
cd quiz_builder
```

### 2. Install Python Dependencies
Make sure you have pipenv installed. If not, install it:

```
pip install pipenv
```

Then install the dependencies:

```
pipenv install
pipenv install strands-agents strands-agents-tools

```

### 3. Set Up and Run Local LLM (via Ollama)
Install Ollama from https://ollama.com, then download the Mistral model:

```
ollama pull mistral
```

Make sure Ollama is running before starting the quiz builder.


### 4. Run the Application with Streamlit
Install Streamlit if needed:

```
pip install streamlit
```

Navigate to the frontend directory and start the app:

```
cd frontend
streamlit run main.py
```

### ✅ Requirements
```
Python 3.8 or later

pipenv

streamlit

Ollama (for running local LLMs)

Mistral model (ollama pull mistral)
```

## 🧑‍💼 Author
Vishal Patoliya

[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vishal-patoliya/)
