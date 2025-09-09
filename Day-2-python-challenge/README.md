# 🦅 Social Eagle - Python Challenge Day 2

#Day 2 : Scenario:
Friends go out for dinner/trip and want to split expenses fairly.

Task:
User enters: total amount + number of people.
Optionally, add each person’s name & contribution.
App calculates how much each person should pay or get back.

> **Welcome to your second Python challenge!** A sophisticated expense management application that demonstrates advanced Streamlit development, data visualization, and real-world problem solving.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red?style=for-the-badge&logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-purple?style=for-the-badge&logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-5.15%2B-green?style=for-the-badge&logo=plotly)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## ✨ Features

### 💸 **Smart Expense Splitting**
- **Multiple Split Types** - Equal split, custom contributions, and percentage-based allocation
- **Optimal Settlement** - Algorithm to minimize transactions between group members
- **Real-time Calculations** - Instant balance updates and validation

### 📊 **Visual Analytics Dashboard**
- **Interactive Charts** - Beautiful Plotly visualizations for expense analysis
- **Balance Overview** - Color-coded indicators (Red=Owes, Green=Gets Back, Gray=Settled)
- **Contribution Analysis** - Pie charts and bar graphs for spending patterns

### 🎨 **Professional UI/UX**
- **Responsive Design** - Works perfectly on mobile and desktop
- **Custom Styling** - Modern cards, gradients, and color schemes
- **Intuitive Navigation** - Tab-based interface with clear user flow

### 📤 **Export & Share**
- **Multiple Formats** - CSV downloads and text summaries
- **WhatsApp Integration** - Ready-to-share settlement messages
- **Data Persistence** - Session state management across tabs

## 🖥️ Screenshots

### Split Calculator Tab
*Intuitive expense entry with multiple split type options*

### Visual Dashboard
*Interactive charts showing balance overview and contribution distribution*

### Export & Share
*WhatsApp-ready messages and CSV downloads for easy sharing*

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone --filter=blob:none --sparse-checkout https://github.com/Shaidhms/se-python-challenge-shaid.git
   cd se-python-challenge-shaid
   git sparse-checkout set Day-2-python-challenge

2. **Install dependencies**
   ```bash
   pip install streamlit streamlit pandas plotly
   ```

3. **Run the application**
   ```bash
   streamlit run splitwise.py
   ```

4. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Start splitting expenses like a pro! 💰
   


## 🎯 How to Use

1. **Enter Expense Details**
- Add total amount and number of people
- Choose your preferred split type
- Add names and contributions (if applicable)

2. **Calculate Split**
- Click "Calculate Split" to see results
- View who owes what with color-coded indicators
- Get optimal settlement suggestions

3. **Analyze with Dashboard**
- Switch to Dashboard tab for visual analysis
- See contribution distributions and balance overviews
- Track spending patterns with interactive charts

4. **Export Results**
- Download CSV files for record keeping
- Generate WhatsApp messages for easy sharing
- Export detailed summaries

## 💡 Use Cases

### 🍽️ **Restaurant Bills**
- Split dinner costs equally or by consumption
- Handle cases where someone pays the full bill
- Account for drinks, appetizers, and individual orders

### ✈️ **Travel Expenses**
- Manage hotel bookings, flights, and activities
- Handle advance payments by different group members
- Split costs for multi-day trips with complex expenses

### 🏠 **Shared Living**
- Split utilities, groceries, and household items
- Manage roommate expenses fairly
- Track monthly recurring costs

### 🎉 **Group Events**
- Split party supplies and venue costs
- Handle group gift purchases
- Manage event planning expenses

## 🧠 What I Learned

This advanced project showcases key concepts in data-driven Python development:

- **Advanced Streamlit** - Multi-tab applications, session state, and custom CSS
- **Data Visualization** - Creating interactive charts with Plotly
- **Pandas Integration** - Data manipulation and CSV export functionality
- **Algorithm Development** - Optimal settlement calculation logic
- **UI/UX Design** - Professional interface design with responsive layouts
- **Real-world Application** - Solving practical problems with code

## 🎨 Customization

### Split Types
The app supports three sophisticated split methods:
- **Equal Split**: Fair division among all participants
- **Custom Contributions**: Handle different payment amounts
- **Percentage Split**: Allocate based on custom percentages

### Visualization Options
- **Balance Charts**: Bar graphs with color-coded balances
- **Pie Charts**: Contribution distribution analysis
- **Metrics Dashboard**: Real-time statistics and summaries

## 🏗️ Project Structure

```
Day-2-python-challenge/
│
├── Day1-Task.py          # Main Streamlit application
├── README.md             # Project documentation  
├── requirements.txt      # Python dependencies
└── .gitignore            # Git ignore rules
```

## 🤝 Contributing

Ready to make SplitWise even better? Here's how:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/expense-categories`)
3. **Implement your improvements** with proper testing
4. **Commit your changes** (`git commit -m 'Add expense categories'`)
5. **Push to your branch** (`git push origin feature/expense-categories`)
6. **Open a Pull Request**

### Ideas for Contributions
- 💱 Multi-currency support
- 📱 Mobile app version
- 🔐 User authentication system
- 📊 Advanced analytics features
- 🎯 Expense categorization
- 📸 Receipt scanning with OCR

## 📝 Requirements

Create a `requirements.txt` file:
```txt
streamlit
pandas
plotly
   ```
## 🏆 Achievements Unlocked

- ✅ Built a complex multi-tab Streamlit application
- ✅ Mastered data visualization with Plotly  
- ✅ Implemented advanced algorithms for optimization
- ✅ Created professional export and sharing features
- ✅ Developed real-world problem-solving skills
- ✅ Learned advanced state management techniques

## 📄 License
This project is licensed under the MIT License 
## 
<div align="center">

**🎓 Keep coding, keep learning!**

Made with ❤️ by **Shaid** using **Streamlit**

⭐ **Star this repo if it helped you learn something new!** ⭐

</div>
