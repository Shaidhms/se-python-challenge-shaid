# 🦅 Social Eagle – Python Challenge Day 11

Day 11 Task :  

Restaurant Order & Billing App 🍔

> Display menu items with prices.

> User selects items + quantity.

> Generate a bill summary (subtotal + tax + total).

> Option to download invoice as CSV/PDF.

# Hyperlane Events — Streamlit Event Registration System

A complete Streamlit app to run events end to end: registrations, QR tickets, voice guidance, multi-currency pricing, waitlists, social sharing, live dashboards, and an admin console. Works with plain CSV files. No external database required.

> Built by **Shaid** for the Social Eagle Python Challenge (Day 11).

# TastyBites — Streamlit Food Ordering Demo 🍔🍕

A polished Streamlit app that lets users browse a menu, add items with add-ons, apply offers, and check out with a UPI QR demo. It exports a PDF invoice, a CSV, and handles promo logic for various deals. The app is built to be responsive for both desktop and mobile views.

<br>

-----

## Demo Video


-----
## ✨ Features

  - **Responsive menu** with categories like Pizza, Burgers, Pasta, Salads, and Drinks.
  - **Add-ons** for each item, displayed in a collapsible expander.
  - **Interactive cart** with live totals, including a 5% GST and a promo code input.
  - **Promotional offers** with specific logic:
      - **`PIZZA10`**: Provides a 10% discount on the base price of pizzas only (excludes add-ons), with a minimum subtotal requirement.
      - **`WELCOME2`**: A "Buy 2 burgers, get 1 free" offer. It adds a free burger to the cart and a corresponding monetary discount to ensure correct totals.
  - **Checkout flow** with a simulated UPI QR payment and a 5-second countdown.
  - **Invoicing** with a PDF invoice (using a safe `Rs` currency symbol to avoid font issues) and a CSV export of the order.
  - **Polished UI** with styled buttons, a carousel for navigation, and improved contrast for better readability.

<br>

-----

## 🧩 Tech Stack

  - **Python 3.11+**
  - **Streamlit**: For building the web application.
  - **ReportLab**: To generate PDF invoices.
  - **QR server API**: To create QR code images without needing an API key.
  - **Plain CSS**: Injected via `st.markdown` for custom styling.

<br>

-----

## 🚀 Quick Start

1.  **Clone the repository:**

    ```sh
    git clone [repository-url]
    cd TastyBites-Streamlit-Demo
    ```

2.  **Create and activate a virtual environment (recommended):**

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # macOS/Linux
    .\venv\Scripts\activate   # Windows PowerShell
    ```

3.  **Install dependencies:**

    ```sh
    pip install streamlit reportlab
    ```

4.  **Run the application:**

    ```sh
    streamlit run app.py
    ```

    The app will open in your browser at `http://localhost:8501`.

<br>

-----

## ⚙️ Configuration

All key configurations are located at the top of the `app.py` file. You can easily customize:

  - **Colors:** Adjust the `PRIMARY_COLOR`, `SECONDARY_COLOR`, etc.
  - **Store details:** Change `STORE_NAME`, `STORE_ADDRESS`, `TAX_RATE`, and `CURRENCY_SYMBOL`.
  - **Menu items and offers:** The `MENU` and `OFFERS` lists can be modified to add, remove, or change items and promotions.

<br>

-----

## 🧾 Invoice & Exports

  - **PDF Invoice:** The app generates PDFs using ReportLab. To ensure proper display, it uses `Rs` instead of the `₹` symbol, which can sometimes have rendering issues with standard fonts like Helvetica. If you need the `₹` symbol, you can switch to a Unicode font (e.g., Noto Sans) and register it with ReportLab.
  - **CSV Export:** A CSV file is also available for download, which includes all line items and final totals.

<br>

-----

## 🧰 Troubleshooting Tips

  - **Buttons require a double-click?** This often happens when `st.rerun()` is used. Check that buttons aren't nested in elements that re-mount on each render and that `st.rerun()` isn't called twice on the same path.
  - **Carousel arrows look wrong?** Ensure that all curly braces `{}` in your CSS f-strings are doubled `{{}}` to prevent formatting errors.
  - **PDF shows squares or junk characters?** This is a font glyph issue. The app uses `Rs` for currency in PDFs to avoid this. If you need the `₹` symbol, you'll need to register a Unicode TTF font with ReportLab.

<br>

-----

## 🤝 Contributing

Contributions are welcome\! Please submit a Pull Request. For UI/CSS changes, be sure to test both desktop and mobile views.

<br>

-----

## 📄 License

This project is licensed under the MIT License.

-----

<div align="center">


🎓 Keep coding, keep learning!
Made with ❤️ by Shaid using Streamlit

⭐ Star this repo if it helped you learn something new! ⭐
