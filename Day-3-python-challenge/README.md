# 🦅 Social Eagle - Python Challenge Day 3

# 🎤 AI Voice Calculator Pro

**Day 3 Python Challenge: Scenario**

Create a smart calculator application that can perform various mathematical operations. The application should be able to accept input both manually and through voice commands, providing a seamless and interactive user experience.

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

## 🚀 Quick Start

### Prerequisites

  - Python 3.8 or higher
  - `pip` package manager

### Installation

1.  **Clone the repository**

    ```bash
    git clone <repository_url>
    cd <repository_folder>
    ```

2.  **Install dependencies**

    ```bash
    pip install streamlit streamlit-audio-recorder SpeechRecognition
    ```

    *Note: For voice recognition to work, you may also need to install `PyAudio` on some systems.*

3.  **Run the application**

    ```bash
    streamlit run app.py
    ```

4.  **Open your browser**

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

\<div align="center"\>

**🎓 Keep coding, keep learning\!**

Made with ❤️ by **Shaid** using **Streamlit**

⭐ **Star this repo if you found it helpful\!** ⭐

\</div\>
