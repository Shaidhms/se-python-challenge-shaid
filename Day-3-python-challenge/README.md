# 🦅 Social Eagle - Python Challenge Day 3

#Day 3 : Scenario:
Simple Calculator ➕➖✖️➗

Inputs: two numbers + operation.

Output: result.

> **Welcome to an advanced Python challenge!** A sophisticated AI-powered calculator that demonstrates cutting-edge Streamlit development, speech recognition integration, and modern user interface design.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red?style=for-the-badge&logo=streamlit)
![Speech Recognition](https://img.shields.io/badge/Speech%20Recognition-3.10%2B-orange?style=for-the-badge&logo=microphone)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-yellow?style=for-the-badge&logo=javascript)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)


## ✨ Features

### 🎙️ **Voice Command Integration**

  - **Speech-to-Text**: Converts spoken commands into text for calculation.
  - **Natural Language Processing**: Parses phrases like "5 plus 5" or "square root of 16."
  - **Auto-Fill**: Automatically populates the calculator fields with parsed numbers and operations.

### 🔢 **Smart Calculation Engine**

  - **Multiple Operations**: Supports addition, subtraction, multiplication, division, power, square root, and percentage.
  - **Real-time Results**: Instantly computes and displays the result after each command.
  - **Error Handling**: Detects and alerts users about errors like division by zero or invalid inputs.

### 📊 **Interactive UI/UX**

  - **Responsive Design**: Works on both desktop and mobile devices.
  - **Modern Interface**: Features a custom AI-themed design with gradients, animations, and color-coded results.
  - **History Log**: Keeps a record of recent calculations for easy reference.

### ⚙️ **Advanced Functionality**

  - **AI Metrics**: Displays simulated AI stats like processing speed and confidence.
  - **Text-to-Speech (Planned)**: Provides a text summary of the calculated result.
  - **Manual Input**: Allows users to enter numbers and select operations manually as an alternative to voice commands.

## 🖥️ Screen Shot 

![6F90DA9B-6C61-4643-A4DD-B4912AACC307_1_102_o](https://github.com/user-attachments/assets/ef84a47a-03cb-4556-8295-cf75caf87c10)


## 🚀 Quick Start

### Prerequisites

  - Python 3.8 or higher
  - `pip` package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone --filter=blob:none --sparse-checkout https://github.com/Shaidhms/se-python-challenge-shaid.git
   cd se-python-challenge-shaid
   git sparse-checkout set Day-3-python-challenge

2. **Install dependencies**
   ```bash
   pip install streamlit SpeechRecognition
   ```

3. **Run the application**
   ```bash
   streamlit run calc.py
   ```

4. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Start using the voice-activated calculator\!

## 🎯 How to Use

1.  **Voice Input**: Click on the microphone icon or the "Record" button to speak your calculation. Examples include:

      - *"What is 10 plus 5?"*
      - *"Calculate 25 times 4."*
      - *"Square root of 81."*

2.  **Manual Input**: Alternatively, type your calculation in the provided text box (e.g., "50 divided by 2").

3.  **Compute**: After entering your command (via voice or text), the calculator will auto-fill the numbers and operation. Click "COMPUTE RESULT" to get your answer.

4.  **View Results**: The result will be displayed in a prominent, color-coded box, along with a summary of the operation.

## 🧠 What I Learned

This project provided a deep dive into the following concepts:

  - **Streamlit Development**: Building a complex, interactive application with dynamic UI elements.
  - **Speech Recognition**: Integrating the `SpeechRecognition` library to handle voice inputs and convert them to text.
  - **Natural Language Processing (NLP)**: Developing a simple parser to extract key information (numbers and operations) from natural language sentences.
  - **Session State Management**: Using `st.session_state` to maintain a history of calculations and pass values between components.
  - **Custom CSS in Streamlit**: Enhancing the application's aesthetics with custom CSS for a professional, branded look.

## 🏗️ Project Structure

```
Day-3-python-challenge/
│
├── calc.py               # Main Streamlit application
├── README.md             # Project documentation  
├── requirements.txt      # Python dependencies
└── .gitignore            # Git ignore rules
```
## 🤝 Contributing

We welcome contributions to make this AI Calculator even better\!

1.  **Fork the repository**.
2.  **Create a new branch** (`git checkout -b feature/your-feature`).
3.  **Commit your changes** (`git commit -am 'Add some feature'`).
4.  **Push to the branch** (`git push origin feature/your-feature`).
5.  **Open a Pull Request**.

### Ideas for Contributions

  - **Text-to-Speech**: Implement a feature to audibly read out the result.
  - **Multi-language Support**: Extend the voice parsing to support other languages.
  - **Advanced Functions**: Add support for trigonometric functions, logarithms, and more complex equations.
  - **Mobile App**: Create a native mobile version using frameworks like `Pydroid 3` or `Kivy`.

## 📄 License

This project is licensed under the MIT License.

## 
<div align="center">

**🎓 Keep coding, keep learning!**

Made with ❤️ by **Shaid** using **Streamlit**

⭐ **Star this repo if it helped you learn something new!** ⭐

</div>

