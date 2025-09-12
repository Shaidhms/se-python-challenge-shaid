# 🦅 Social Eagle - Python Challenge Day 5

#Day 5 :
Unit Converter 🔄

Convert: currency, temperature, length, weight.

Show results instantly.

> **Welcome to your 5th Python challenge\!** Unit Convertor with AI recommendations for best exchange center.A minimalist and fast-paced Streamlit application designed for all your conversion needs.  
This app provides **live, accurate currency exchange rates**, along with converters for **temperature, length, and weight.Built with simplicity and speed in mind, it offers **instant results without any buttons**, updating automatically as you type.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)


## ✨ Features

### 💱 Currency Converter
- **Live Rates:** Fetches live mid-market exchange rates from a public, no-key API with a fallback system.  
- **Failover Logic:** Automatically switches from the primary Frankfurter API to the Open ER API if the first one fails.  
- **Historical Data:** View a 5-year history of exchange rates with an interactive chart.  
- **AI Integration:** Generates a custom ChatGPT prompt to help you find the best local cash exchange centers.  

### 🌡️ Temperature Converter
- Converts between **Celsius (°C)**, **Fahrenheit (°F)**, and **Kelvin (K)**.  
- Includes fun, relatable facts about the converted temperature for extra context.  

### 📏 Length Converter
Supports:
- **m**, **cm**, **mm**, **km**, **in**, **ft**, **yd**, **mi**  
Conversions are based on meters for precision.  

### ⚖️ Weight Converter
Supports:
- **g**, **kg**, **lb**, **oz**, **tonnes**  
Conversions are based on grams for precision.  

### ⚡ Performance & UI
- **Instant Updates:** Real-time calculations — no "Convert" button needed.  
- **Responsive Design:** Clean, two-column grid layout optimized for both desktop and mobile.  
- **Custom Theming:** Toggle between **light** and **dark** modes with polished custom CSS.  

---

## 🚀 Quick Start

### Prerequisites
- Python **3.8+**
- `pip` package manager  

### Installation
Clone the repository:
```bash
git clone https://github.com/Shaidhms/se-python-challenge-shaid.git
cd se-python-challenge-shaid/Day-5-python-challenge
```

Note: The project uses a sparse-checkout strategy to focus on a single day’s challenge.
If you cloned the main repository, navigate to the Day-5-python-challenge directory.

Install dependencies:
```bash
pip install -r requirements.txt
```
Or manually install:
```bash
pip install streamlit requests pytz python-dotenv pandas
```
Run the app:
```bash
streamlit run app.py
```
Open your browser at http://localhost:8501.

⸻

📂 Project Structure
```
Day-5-python-challenge/
│
├── app.py             # Main Streamlit application
├── README.md          # Project documentation
├── requirements.txt   # Python dependencies
└── .env               # Optional: API key configuration
```
⸻

### 🔐 Optional: OpenAI Integration

### To use the “Locate Best Exchange Centers” feature:
	1.	Create a .env file in the project directory.
	2.	Add your OpenAI API key:

**OPENAI_API_KEY=sk-...



This feature does not call OpenAI unless you explicitly click the button.
It simply prepares a copyable prompt for your convenience.

⸻

🤝 Contributing

Contributions are welcome!
	1.	Fork the repo.
	2.	Create a new branch:
	 
```bash
	git checkout -b feature/add-new-units
```
	3.	Make your changes and test them thoroughly.
	4.	Commit your changes with a clear message:
 
```bash
git commit -m 'Add new units to length converter'
```
	5.	Push your branch:
```bash
git push origin feature/add-new-units

```
	6.	Open a Pull Request.

⸻

📄 License

This project is licensed under the MIT License.

⸻

<div align="center"\>

**🎓 Keep coding, keep learning\!**

Made with ❤️ by **Shaid** using **Streamlit**

⭐ **Star this repo if it helped you learn something new\!** ⭐

</div>
