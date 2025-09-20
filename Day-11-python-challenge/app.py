import streamlit as st
import time
from decimal import Decimal, ROUND_HALF_UP
import base64
from io import BytesIO, StringIO
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
import os
from typing import Optional
from urllib.parse import quote_plus

import base64


def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_image("se.png")

st.markdown(
    f"""
    <h2 class="main-header">
        <center>  <img src="data:image/png;base64,{logo_base64}" width="40" style="vertical-align: middle; margin-left:5px;"></center>
           <center> Social Eagle Python Challenge </center>
        <center> Day 11 - Restaurant Order & Billing App</center>
    </h2>
    """,
    unsafe_allow_html=True
)
# ---------------------------
# CONFIGURATION & ASSETS
# ---------------------------

# Colors (easily tweakable)
PRIMARY_COLOR = "#FF4B3E"
SECONDARY_COLOR = "#FFC857"
ACCENT_COLOR = "#2EC4B6"
NEUTRAL_COLOR = "#1F2937"
SURFACE_DARK = "#111827"
SURFACE_LIGHT = "#F9FAFB"

# Store Config
STORE_NAME = "TastyBites"
STORE_ADDRESS = "Pudupakkam, Chennai, 600103"
TAX_RATE = Decimal("0.05")  # 5%
CURRENCY_SYMBOL = "₹"  # Change as needed (e.g., $, €)

# Placeholder animated assets (public domain / royalty-free)
# Replace with your own GIF/WebP URLs or local paths
ASSETS = {
    "pizza_margherita": "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3MXN4M2szMGliYnk4bmk3bXB1YjU2M3pkdm45dmFsamJhcnNqanVvbSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/KsMP4vmlDYVpu/giphy.gif",
    "burger_classic": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExa3oyb3VnazVwaHU3ZzNtdWd1dms3YzQyN3NsNWk2d21yazMzOHM5ZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/XXsyB8OWePXva/giphy.gif",
    "pasta_bolognese": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzZkYXI1MjVvaTF1bHZpZm5lMWt3OXh1aTBvZWtxdXN6NXBqd3lyeSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/SKcoBSBFE51TO/giphy.gif",
    "salad_caesar": "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3bHp3eXhqMDAweXdrN3NpYWp2MnV5YTl3dXVueWpvZ3prdGl1ZXljZiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/RBkEGyrZD16P6/giphy.gif",  # reuse for demo
    "soda_cola": "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3NWwyN24wYnYwdG51MGl6dGFzaGZ5MnZmbHlvMmxwcDRxdXFmN2E0eSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/xNmFlpxwNoRtm/giphy.gif",  # reuse
    #"offer_banner_2": "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3aWllaGJ1cHlzMWxjNDIxbDI2MHVyeGhqNTJkZ3NucTlmb2lvNjc4dyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/9KCNcFVQmZhRK/giphy.gif",
    "offer_banner_1": "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3aWRwY3FnaHp3NmUxeDE5ZG5nemFnaXh1eTNrYXYwbjRqNWg4OXp4NiZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/3osxY7nhAHq7gOBIiY/giphy.gif",
   # "offer_banner_2":"https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3dGw5MmE2YWdkcDUxN2dqa3A2c3pvbWJ5N20yOWxoYnNxbmxsOTV1YyZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/VEmknYXxzxflAUEQmI/giphy.gif",
    "offer_banner_2":"https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaTlwZ201bm8xeGV2N2o5NzJqZmtsenExMnBwNmhtcjhocXlrd2JuMiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/PM3ovusoQcCQqMPVLi/giphy.gif",
    "pizza_veg": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMHczaWQ3dzRuODFrZGs3OGtmY2trZGJobTM3dGs3aWJla2s1cGRqeSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/GFKZLvfBiyrN6/giphy.gif"
}

# Fallback static image if GIF fails
FALLBACK_IMAGE = "https://via.placeholder.com/300x200?text=Food+Image"

# Offers Configuration
OFFERS = [
    {
        "code": "PIZZA10",
        "label": "10% OFF Pizzas",
        "percent_off": 10,
        "min_subtotal": 20.00,
        "banner_img": ASSETS["offer_banner_1"],
        "active": True
    },
    {
        "code": "WELCOME2",
        "label": "By 2 Get 1 Free",
        "percent_off": 5,
        "min_subtotal": 10.00,
        "banner_img": ASSETS["offer_banner_2"],
        "active": True
    }
]

# Sample Menu Data
MENU = [
    {
        "id": "mx01",
        "name": "Classic Margherita Pizza",
        "category": "Pizza",
        "desc": "San Marzano tomatoes, fresh mozzarella, basil, olive oil",
        "price": 499,
        "veg": True,
        "rating": 4.6,
        "img": ASSETS["pizza_margherita"],
        "addons": [
            {"id": "ad01", "name": "Extra Cheese", "price": 10},
            {"id": "ad02", "name": "Olives", "price": 60},
            {"id": "ad03", "name": "Pepperoni", "price": 10}
        ]
    },
    {
        "id": "mx02",
        "name": "Classic Chicken Burger",
        "category": "Burgers",
        "desc": "Juicy Chicken patty, lettuce, tomato, pickles, special sauce",
        "price": 89,
        "veg": False,
        "rating": 4.3,
        "img": ASSETS["burger_classic"],
        "addons": [
            {"id": "ad04", "name": "Cheese", "price": 10},
            {"id": "ad05", "name": "Avocado", "price": 20}
        ]
    },
    {
        "id": "mx03",
        "name": "Spaghetti Bolognese",
        "category": "Pasta",
        "desc": "Homemade pasta with rich meat sauce and parmesan",
        "price": 99,
        "veg": False,
        "rating": 4.7,
        "img": ASSETS["pasta_bolognese"],
        "addons": [
            {"id": "ad06", "name": "Extra Meat", "price": 22},
            {"id": "ad07", "name": "Garlic Bread", "price": 11}
        ]
    },
    {
        "id": "mx04",
        "name": "Caesar Salad",
        "category": "Salads",
        "desc": "Romaine, croutons, parmesan, caesar dressing",
        "price": 169,
        "veg": True,
        "rating": 4.2,
        "img": ASSETS["salad_caesar"],
        "addons": [
            {"id": "ad08", "name": "Grilled Chicken", "price": 30},
            {"id": "ad09", "name": "Shrimp", "price": 40}
        ]
    },
    {
        "id": "mx05",
        "name": "Cola",
        "category": "Drinks",
        "desc": "Chilled cola in a glass bottle",
        "price": 49,
        "veg": True,
        "rating": 4.0,
        "img": ASSETS["soda_cola"],
        "addons": [
            {"id": "ad11", "name": "Extra Ice", "price": 3},
            {"id": "ad12", "name": "Lemon Slice", "price": 4},
            {"id": "ad13", "name": "Large Size (500ml)", "price": 5.50},
            {"id": "ad14", "name": "Paper Straw", "price": 3}
        ]
    },
    {
        "id": "mx06",
        "name": "Veggie Pizza",
        "category": "Pizza",
        "desc": "Loaded with bell peppers, onions, mushrooms, olives, corn",
        "price": 399,
        "veg": True,
        "rating": 4.5,
        "img": ASSETS["pizza_veg"],  # reuse
        "addons": [
            {"id": "ad01", "name": "Extra Cheese", "price": 10},
            {"id": "ad10", "name": "Jalapeños", "price": 70}
        ]
    }
]

CATEGORIES = sorted(list(set(item["category"] for item in MENU)))

# ---------------------------
# SESSION STATE INIT
# ---------------------------

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "promo_code" not in st.session_state:
    st.session_state.promo_code = ""

if "applied_discount" not in st.session_state:
    st.session_state.applied_discount = Decimal("0.00")

if "valid_promo" not in st.session_state:
    st.session_state.valid_promo = None

if "carousel_index" not in st.session_state:
    st.session_state.carousel_index = 0

if "last_tick" not in st.session_state:
    st.session_state.last_tick = time.time()

# Track promo quantity adjustments so they are only applied once per promo code
if "promo_qty_applied" not in st.session_state:
    st.session_state.promo_qty_applied = {}

# Payment session state
if "payment_success" not in st.session_state:
    st.session_state.payment_success = False
if "payment_started_at" not in st.session_state:
    st.session_state.payment_started_at = None
if "payment_window_secs" not in st.session_state:
    st.session_state.payment_window_secs = 5  # demo: 5‑second countdown
if "show_invoice" not in st.session_state:
    st.session_state.show_invoice = False

# ---------------------------
# HELPER FUNCTIONS
# ---------------------------

# ---- Query param helper (handles older/newer Streamlit) ----
def get_query_param(name: str, default: Optional[str] = None):
    try:
        # Newer Streamlit
        val = st.query_params.get(name)
        if val is None:
            return default
        return val
    except Exception:
        # Older Streamlit API
        try:
            qp = st.experimental_get_query_params()
            if name in qp and len(qp[name]) > 0:
                return qp[name][0]
        except Exception:
            pass
        return default


def format_currency(amount):
    """Format Decimal amount to currency string."""
    return f"{CURRENCY_SYMBOL}{amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}"

# Use ASCII-friendly currency for PDF to avoid missing glyphs in Helvetica
def format_currency_pdf(amount: Decimal) -> str:
    return f"Rs {amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}"

def get_offer_by_code(code):
    """Return offer dict if code is valid and active."""
    code = code.strip().upper()
    for offer in OFFERS:
        if offer["code"] == code and offer["active"]:
            return offer
    return None

def compute_totals():
    """Compute subtotal, tax, discount, and grand total from cart.
    - PIZZA10: 10% off *pizza base price only* (excludes add-ons), if min subtotal met
    - WELCOME2: visual free burger(s) handled in render_cart(); no price change here unless you later want to convert to a monetary discount
    """
    subtotal = Decimal("0.00")
    pizza_base_subtotal = Decimal("0.00")

    for item_id, item_data in st.session_state.cart.items():
        qty = item_data["qty"]
        unit_price = Decimal(str(item_data["price"]))
        addon_total = sum(Decimal(str(a["price"])) for a in item_data.get("addons", []))
        # line total includes add-ons
        line_total = (unit_price + addon_total) * qty
        subtotal += line_total
        # pizza base (no add-ons) for pizza-only percentage discounts
        if item_data.get("category") == "Pizza":
            pizza_base_subtotal += (unit_price * qty)

    # Apply discount if valid
    discount = Decimal("0.00")
    offer = st.session_state.valid_promo
    if offer:
        code = offer.get("code", "").upper()
        min_needed = Decimal(str(offer.get("min_subtotal", 0)))
        if subtotal >= min_needed:
            if code == "PIZZA10":
                # 10% off on pizza base value only
                percent = Decimal("10")
                discount = (pizza_base_subtotal * percent / Decimal("100")).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            elif code == "WELCOME2":
                # Buy 2 get 1 free (burgers): give one burger base price free per pair
                burger_items = [(iid, data) for iid, data in st.session_state.cart.items() if data.get("category") == "Burgers"]
                total_burger_qty = sum(int(d.get("qty", 0)) for _, d in burger_items)
                if total_burger_qty >= 2:
                    free_count = total_burger_qty // 2
                    # Choose a representative burger price: the one with the highest qty in cart
                    chosen_price = Decimal("0")
                    if burger_items:
                        chosen = max(burger_items, key=lambda t: int(t[1].get("qty", 0)))[1]
                        chosen_price = Decimal(str(chosen.get("price", 0)))
                    discount = (chosen_price * free_count).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                else:
                    discount = Decimal("0.00")
            else:
                # Fallback to generic percent off whole cart if configured
                percent = Decimal(str(offer.get("percent_off", 0)))
                discount = (subtotal * percent / Decimal("100")).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    tax = ((subtotal - discount) * TAX_RATE).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    grand_total = (subtotal - discount + tax).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    return subtotal, discount, tax, grand_total

def add_to_cart(item_id, qty=1, addons=None):
    """Add, update, or remove item in cart.
    - qty == 0  -> remove item if present
    - 1 <= qty <= 20 -> add/update
    """
    # Handle remove explicitly
    if qty == 0:
        if item_id in st.session_state.cart:
            del st.session_state.cart[item_id]
        return

    # Guard invalid values
    if qty < 0:
        return
    if qty > 20:
        st.warning(f"Max quantity is 20 for {item_id}.")
        qty = 20

    # Find the menu item
    menu_item = next((item for item in MENU if item["id"] == item_id), None)
    if not menu_item:
        return

    # Create entry if not exists
    if item_id not in st.session_state.cart:
        st.session_state.cart[item_id] = {
            "name": menu_item["name"],
            "category": menu_item["category"],
            "price": menu_item["price"],
            "qty": 0,
            "addons": []
        }

    # Update
    st.session_state.cart[item_id]["qty"] = qty
    if addons is not None:
        st.session_state.cart[item_id]["addons"] = addons

def make_csv():
    """Generate CSV from current cart."""
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Item", "Category", "Qty", "Unit Price", "Add-ons", "Line Total"])

    for item_id, item_data in st.session_state.cart.items():
        addons_str = "; ".join([f"{a['name']} (+{CURRENCY_SYMBOL}{a['price']})" for a in item_data.get("addons", [])])
        unit_price = Decimal(str(item_data["price"]))
        addon_total = sum(Decimal(str(a["price"])) for a in item_data.get("addons", []))
        line_total = (unit_price + addon_total) * item_data["qty"]
        writer.writerow([
            item_data["name"],
            item_data["category"],
            item_data["qty"],
            f"{CURRENCY_SYMBOL}{unit_price}",
            addons_str,
            f"{CURRENCY_SYMBOL}{line_total.quantize(Decimal('0.01'))}"
        ])

    subtotal, discount, tax, grand_total = compute_totals()
    writer.writerow([])
    writer.writerow(["Subtotal", "", "", "", "", format_currency(subtotal)])
    if discount > 0:
        writer.writerow(["Discount", "", "", "", "", f"-{format_currency(discount)}"])
    writer.writerow(["GST", "", "", "", "", format_currency(tax)])
    writer.writerow(["Grand Total", "", "", "", "", format_currency(grand_total)])

    return output.getvalue()

def make_pdf():
    """Generate PDF invoice using ReportLab."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor(PRIMARY_COLOR),
        spaceAfter=12
    )
    normal_style = styles['Normal']
    bold_style = ParagraphStyle('Bold', parent=styles['Normal'], fontName='Helvetica-Bold')

    # Store Header
    elements.append(Paragraph(STORE_NAME, title_style))
    elements.append(Paragraph(STORE_ADDRESS, normal_style))
    elements.append(Spacer(1, 0.2*inch))

    # Invoice Info
    invoice_number = f"INV-{int(time.time())}"
    elements.append(Paragraph(f"Invoice #: {invoice_number}", normal_style))
    elements.append(Paragraph(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    elements.append(Spacer(1, 0.3*inch))

    # Table Header
    data = [["Item", "Qty", "Unit Price", "Add-ons", "Line Total"]]

    for item_id, item_data in st.session_state.cart.items():
        addons_str = "; ".join([f"{a['name']} (+{CURRENCY_SYMBOL}{a['price']})" for a in item_data.get("addons", [])])
        unit_price = Decimal(str(item_data["price"]))
        addon_total = sum(Decimal(str(a["price"])) for a in item_data.get("addons", []))
        line_total = (unit_price + addon_total) * item_data["qty"]
        data.append([
            item_data["name"],
            str(item_data["qty"]),
            format_currency_pdf(unit_price),
            addons_str,
            format_currency_pdf(line_total)
        ])

    # Create table
    table = Table(data, colWidths=[2*inch, 0.6*inch, 0.8*inch, 1.5*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(PRIMARY_COLOR)),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('ALIGN', (1,1), (1,-1), 'CENTER'),
        ('ALIGN', (2,1), (4,-1), 'RIGHT'),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))

    # Totals
    subtotal, discount, tax, grand_total = compute_totals()
    elements.append(Paragraph(f"Subtotal: {format_currency_pdf(subtotal)}", bold_style))
    if discount > 0:
        elements.append(Paragraph(f"Discount: -{format_currency_pdf(discount)}", bold_style))
    elements.append(Paragraph(f"GST ({int(TAX_RATE*100)}%): {format_currency_pdf(tax)}", bold_style))
    elements.append(Paragraph(f"Grand Total: {format_currency_pdf(grand_total)}", ParagraphStyle('GrandTotal', parent=bold_style, fontSize=14, textColor=colors.HexColor(PRIMARY_COLOR))))

    # Footer
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("Thank you for your order!", normal_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# ---------------------------
# UI COMPONENTS
# ---------------------------

def render_header():
    """Render app header with logo and title."""
    st.markdown(f"""
        <div style="text-align: center; padding: 1rem 0; background: linear-gradient(135deg, {PRIMARY_COLOR}, {SECONDARY_COLOR}); color: white; border-radius: 12px; margin-bottom: 1rem;">
            <h1 style="margin: 0; font-size: 2.5rem; font-family: 'Poppins', sans-serif;">{STORE_NAME}</h1>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;">Delicious food delivered to your door</p>
        </div>
    """, unsafe_allow_html=True)

def render_offers_carousel():
    """Render rotating offer carousel."""
    active_offers = [offer for offer in OFFERS if offer["active"]]
    if not active_offers:
        return

    # Manual controls (no auto-rerun)
    idx = st.session_state.carousel_index % len(active_offers)
    current_offer = active_offers[idx]

    st.markdown(f"""
        <div class="carousel-wrapper" style="position: relative; margin: 1rem 0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <img src="{current_offer['banner_img']}" 
                 onerror="this.src='{FALLBACK_IMAGE}';" 
                 style="width: 100%; height: auto; display: block; animation: pulse 2s infinite;">
            <div style="position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.7); color: white; padding: 0.5rem 1rem;">
                <strong>{current_offer['label']}</strong> — Use code: <code>{current_offer['code']}</code>
            </div>
        </div>
        <style>
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.8; }}
            100% {{ opacity: 1; }}
        }}
        </style>
    """, unsafe_allow_html=True)

    # Streamlit-native controls below the banner (reliable state updates)
    st.markdown('<div class="carousel-nav">', unsafe_allow_html=True)
    nav = st.columns([1, 8, 0.5])
    with nav[0]:
        if st.button("◀", key="offer_prev", help="Previous offer"):
            st.session_state.carousel_index = (idx - 1) % len(active_offers)
            st.rerun()
    with nav[2]:
        if st.button("▶", key="offer_next", help="Next offer"):
            st.session_state.carousel_index = (idx + 1) % len(active_offers)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def render_menu_grid():
    """Render menu items in a responsive grid."""
    # Category filter (single dropdown)
    selected_category = st.selectbox("Filter by Category", ["All"] + CATEGORIES, key="category_filter")

    # Filter menu (robust to case/whitespace)
    if selected_category == "All":
        filtered_menu = MENU
    else:
        sel = selected_category.strip().lower()
        filtered_menu = [item for item in MENU if item["category"].strip().lower() == sel]

    # Grid layout
    cols = st.columns(2) if st.session_state.get("viewport", "desktop") == "mobile" else st.columns(3)

    for idx, item in enumerate(filtered_menu):
        with cols[idx % len(cols)]:
            render_menu_item(item)

def render_menu_item(item):
    """Render a single menu item card."""
    with st.container():
        st.markdown(f"""
            <div class="menu-card" style="
                background: white;
                border-radius: 16px;
                padding: 1rem;
                margin-bottom: 1rem;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                border: 1px solid #eee;
                min-height: 340px; display: flex; flex-direction: column; justify-content: flex-start;
            ">
                <div style="text-align: center; margin-bottom: 0.5rem;">
                    <img src="{item['img']}" 
                         onerror="this.src='{FALLBACK_IMAGE}';"
                         style="width: 100%; height: 150px; object-fit: cover; border-radius: 12px; animation: float 3s ease-in-out infinite;">
                </div>
                <h4 style="margin: 0.5rem 0 0.25rem 0; color: {NEUTRAL_COLOR}; font-family: 'Poppins', sans-serif;">{item['name']}</h4>
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <span style="color: #FFD700;">{'★' * int(item['rating'])}{'☆' * (5 - int(item['rating']))}</span>
                    <span style="font-size: 0.85rem; color: #666;">({item['rating']})</span>
                    <span style="margin-left: auto; font-weight: bold; color: {PRIMARY_COLOR};">{CURRENCY_SYMBOL}{item['price']}</span>
                </div>
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    {'<span style="color: green; font-weight: bold;">🌱 Veg</span>' if item['veg'] else '<span style="color: red; font-weight: bold;">🥩 Non-Veg</span>'}
                </div>
                <p style="font-size: 0.85rem; color: #555; margin: 0.5rem 0; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; min-height: 2.6em;">{item['desc']}</p>
            </div>
            <style>
            @keyframes float {{
                0% {{ transform: translateY(0px); }}
                50% {{ transform: translateY(-5px); }}
                100% {{ transform: translateY(0px); }}
            }}
            .menu-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 16px rgba(0,0,0,0.15);
            }}
            </style>
        """, unsafe_allow_html=True)

        # Add-ons
        addon_selections = []
        if item["addons"]:
            with st.expander("Add-ons", expanded=False):
                for addon in item["addons"]:
                    selected = st.checkbox(f"{addon['name']} (+{CURRENCY_SYMBOL}{addon['price']})", key=f"addon_{item['id']}_{addon['id']}")
                    if selected:
                        addon_selections.append(addon)

        # Quantity and Add to Cart
        col1, col2 = st.columns([3,1])
        with col1:
            qty = st.number_input("Qty", min_value=0, max_value=20, value=1, key=f"qty_{item['id']}", label_visibility="collapsed")
        with col2:
            if st.button("Add", key=f"add_{item['id']}", use_container_width=True):
                add_to_cart(item["id"], qty, addon_selections)
                st.toast(f"Added {item['name']} to cart — showing cart", icon="🛒")
                st.markdown("""
                    <script>
                      const c = document.getElementById('cart-container');
                      if (c) { c.scrollIntoView({behavior: 'smooth', block: 'start'}); }
                    </script>
                """, unsafe_allow_html=True)

        st.markdown("---")

def render_cart():
    """Render sticky cart panel."""
    if not st.session_state.cart:
        return

    # Determine layout: side panel on desktop, bottom sheet on mobile
    is_mobile = st.session_state.get("viewport", "desktop") == "mobile"

    cart_container_style = """
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 1rem;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        z-index: 12;
        border-top-left-radius: 16px;
        border-top-right-radius: 16px;
        max-height: 80vh;
        overflow-y: auto;
    """ if is_mobile else """
        position: fixed;
        top: 100px;
        right: 20px;
        width: 320px;
        background: white;
        padding: 1rem;
        box-shadow: -2px 2px 12px rgba(0,0,0,0.1);
        border-radius: 16px;
        z-index: 12;
        max-height: 70vh;
        overflow-y: auto;
    """

    # st.markdown(f"""
    #     <div id="cart-container" style="{cart_container_style}">
    # """, unsafe_allow_html=True)

    # Cart heading (compact)
    item_count = sum(int(v.get("qty", 0)) for v in st.session_state.cart.values())
    st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:0.5rem;">
            <h4 style="margin:0; color:{PRIMARY_COLOR};">Items in Cart</h4>
            <span style="background:{SECONDARY_COLOR}; color:{NEUTRAL_COLOR}; padding:0.15rem 0.5rem; border-radius:12px; font-weight:600;">{item_count}</span>
        </div>
    """, unsafe_allow_html=True)

    # Cart Items
    for item_id, item_data in list(st.session_state.cart.items()):
        with st.container():
            col1, col2, col3 = st.columns([3,1,1])
            with col1:
                st.markdown(f"**{item_data['name']}**")
                if item_data.get("addons"):
                    addons_str = ", ".join([a["name"] for a in item_data["addons"]])
                    st.markdown(f"<small style='color: #666;'>+ {addons_str}</small>", unsafe_allow_html=True)
            with col2:
                new_qty = st.number_input("Qty", min_value=0, max_value=20, value=item_data["qty"], key=f"cart_qty_{item_id}", label_visibility="collapsed")
                if new_qty != item_data["qty"]:
                    add_to_cart(item_id, new_qty, item_data.get("addons"))
            with col3:
                unit_price = Decimal(str(item_data["price"]))
                addon_total = sum(Decimal(str(a["price"])) for a in item_data.get("addons", []))
                line_total = (unit_price + addon_total) * item_data["qty"]
                st.markdown(f"**{format_currency(line_total)}**")
                if st.button("❌", key=f"remove_{item_id}", help="Remove item"):
                    add_to_cart(item_id, 0)
                    st.rerun()

    # Visual freebies for WELCOME2 (Buy 2 Get 1 Free on Burgers)
    if st.session_state.valid_promo and st.session_state.valid_promo.get("code", "").upper() == "WELCOME2":
        burger_items = [(iid, data) for iid, data in st.session_state.cart.items() if data.get("category") == "Burgers"]
        total_burger_qty = sum(int(d.get("qty", 0)) for _, d in burger_items)
        if total_burger_qty >= 2:
            free_count = total_burger_qty // 2  # one free per 2 purchased
            # Choose the burger item to display as free: the one with highest qty
            chosen = None
            if burger_items:
                chosen = max(burger_items, key=lambda t: int(t[1].get("qty", 0)))[1]
            if chosen and free_count > 0:
                unit_price = Decimal(str(chosen["price"]))
                st.markdown(
                    f"""
                    <div style="display:flex; align-items:center; justify-content:space-between; padding:0.25rem 0;">
                        <div style="font-weight:600; color:{PRIMARY_COLOR};">FREE (WELCOME2): {chosen['name']} × {free_count}</div>
                        <div style="text-align:right;">
                            <span style="color:#999; text-decoration: line-through; margin-right:6px;">{format_currency(unit_price)}</span>
                            <span style="font-weight:700;">{format_currency(Decimal('0'))}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("---")

    # Promo Code
    promo_input = st.text_input("Promo Code", value=st.session_state.promo_code, key="promo_input", placeholder="Enter code")
    if promo_input != st.session_state.promo_code:
        st.session_state.promo_code = promo_input
        offer = get_offer_by_code(promo_input)
        if offer:
            st.session_state.valid_promo = offer
            st.markdown(
                f"""
                <div style="background:#D1FAE5; color:{NEUTRAL_COLOR}; padding:0.75rem 1rem; border-radius:12px; font-weight:600;">
                    🎉 {offer['label']} applied!
                </div>
                """,
                unsafe_allow_html=True,
            )
            # If WELCOME2 is applied, add free burger quantity directly to cart once
            code = offer.get("code", "").upper()
            if code == "WELCOME2" and not st.session_state.promo_qty_applied.get(code):
                # Calculate total burgers and free count
                burger_items = [(iid, data) for iid, data in st.session_state.cart.items() if data.get("category") == "Burgers"]
                total_burger_qty = sum(int(d.get("qty", 0)) for _, d in burger_items)
                free_count = total_burger_qty // 2
                if free_count > 0 and burger_items:
                    # Choose the burger with the highest qty to receive the free units
                    chosen_id, chosen = max(burger_items, key=lambda t: int(t[1].get("qty", 0)))
                    st.session_state.cart[chosen_id]["qty"] = int(st.session_state.cart[chosen_id]["qty"]) + free_count
                    # Mark as adjusted so we don't double-add on rerun
                    st.session_state.promo_qty_applied[code] = free_count
                    # Inform user
                    st.toast(f"WELCOME2 applied: added {free_count} free burger(s) to your cart.", icon="🍔")
                    st.rerun()
        else:
            st.session_state.valid_promo = None
            if promo_input.strip():
                st.error("❌ Invalid promo code")

    # Totals
    subtotal, discount, tax, grand_total = compute_totals()

    st.markdown(f"**Subtotal:** {format_currency(subtotal)}")
    if discount > 0:
        st.markdown(f"**Discount:** -{format_currency(discount)}")
    st.markdown(f"**GST ({int(TAX_RATE*100)}%):** {format_currency(tax)}")
    st.markdown(f"<h3 style='color: {PRIMARY_COLOR}; margin: 0.5rem 0;'>**Total: {format_currency(grand_total)}**</h3>", unsafe_allow_html=True)

    # Checkout Button
    if st.button("💳 Review & Checkout", use_container_width=True, key="checkout_btn"):
        # Start payment flow
        st.session_state.show_checkout = True
        st.session_state.payment_success = False
        st.session_state.payment_started_at = None
        st.session_state.show_invoice = False
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Floating Checkout Button (Desktop only)
    if not is_mobile and st.session_state.cart:
        st.markdown(
            f"""
            <a id=\"float-checkout\" href=\"#\" class=\"animate-bounce\" style=\"
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: {PRIMARY_COLOR};
                color: white;
                padding: 0.75rem 1.5rem;
                border-radius: 50px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                font-weight: bold;
                z-index: 999;
                cursor: pointer;
                text-decoration: none;\">
                💳 Checkout ({format_currency(grand_total)})
            </a>
            <script>
              const fc = document.getElementById('float-checkout');
              if (fc) {{
                fc.addEventListener('click', function(e) {{
                  e.preventDefault();
                  const btns = Array.from(document.querySelectorAll('button'));
                  const target = btns.find(b => b.innerText && b.innerText.trim().includes('Review & Checkout'));
                  if (target) {{ target.click(); }}
                }});
              }}
            </script>
            """,
            unsafe_allow_html=True,
        )

def render_payment():
    """Show UPI QR, countdown, and auto-success with 'Check Invoice' button."""
    st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: {SURFACE_LIGHT}; border-radius: 12px; margin-bottom: 1rem;">
            <h2 style="color: {PRIMARY_COLOR}; margin: 0;">UPI Payment</h2>
            <p style="margin: 0.5rem 0 0 0;">Scan to pay with any UPI app</p>
        </div>
    """, unsafe_allow_html=True)

    # Amount due
    subtotal, discount, tax, grand_total = compute_totals()
    st.markdown(f"<h4 style='text-align:center;margin:0 0 0.5rem 0;'>Amount Due: {format_currency(grand_total)}</h4>", unsafe_allow_html=True)

    # Build a sample UPI intent and QR code URL
    upi_intent = f"upi://pay?pa=tastybites@upi&pn=TastyBites&am={grand_total}&cu=INR&tn=TastyBites%20Order"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&data={quote_plus(upi_intent)}"
    st.markdown(f"<div style='text-align:center;'><img src='{qr_url}' width='220' height='220' alt='UPI QR'/></div>", unsafe_allow_html=True)
   # st.markdown(f"<div style='margin:8px auto;max-width:640px;background:#1118270D;color:{NEUTRAL_COLOR};padding:8px 12px;border-radius:8px;font-family:ui-monospace, SFMono-Regular, Menlo, monospace;word-break:break-all;'>{upi_intent}</div>", unsafe_allow_html=True)

    # Countdown handling
    if not st.session_state.payment_success:
        if not st.session_state.payment_started_at:
            st.session_state.payment_started_at = time.time()
        elapsed = time.time() - st.session_state.payment_started_at
        total = st.session_state.payment_window_secs
        remaining = max(0, int(total - elapsed))
        # Simple progress
        prog = st.progress(min(1.0, elapsed / total))
        st.markdown(f"<p style='text-align:center;'>Waiting for payment confirmation… <strong>{remaining}s</strong></p>", unsafe_allow_html=True)
        if remaining <= 0:
            st.session_state.payment_success = True
            st.rerun()
        else:
            time.sleep(1)
            st.rerun()
    else:
        st.markdown(
            f"""
            <div style="background:#D1FAE5; color:{NEUTRAL_COLOR}; padding:0.75rem 1rem; border-radius:12px; font-weight:700; text-align:center;">
                \nPayment successful! 🎉 Your order has been placed.
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Actions
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            if st.button("Check Invoice", use_container_width=True):
                st.session_state.show_invoice = True
                st.rerun()
        st.markdown("<div style='text-align:center;margin-top:0.5rem;'>Didn’t receive a prompt? You can also <em>resend UPI</em> below.</div>", unsafe_allow_html=True)
        _, mid, _ = st.columns([1,2,1])
        with mid:
            if st.button("Resend UPI Request", use_container_width=True):
                st.session_state.payment_success = False
                st.session_state.payment_started_at = None
                st.rerun()

def render_invoice():
    """Render invoice view."""
    st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: {SURFACE_LIGHT}; border-radius: 12px; margin-bottom: 1rem;">
            <h2 style="color: {PRIMARY_COLOR}; margin: 0;">🧾 Invoice</h2>
            <p style="margin: 0.5rem 0 0 0;">{STORE_NAME}</p>
            <p style="margin: 0;">{STORE_ADDRESS}</p>
        </div>
    """, unsafe_allow_html=True)

    # Invoice Items
    for item_id, item_data in st.session_state.cart.items():
        with st.container():
            col1, col2 = st.columns([3,1])
            with col1:
                st.markdown(f"**{item_data['name']}** × {item_data['qty']}")
                if item_data.get("addons"):
                    addons_str = ", ".join([a["name"] for a in item_data["addons"]])
                    st.markdown(f"<small>+ {addons_str}</small>", unsafe_allow_html=True)
            with col2:
                unit_price = Decimal(str(item_data["price"]))
                addon_total = sum(Decimal(str(a["price"])) for a in item_data.get("addons", []))
                line_total = (unit_price + addon_total) * item_data["qty"]
                st.markdown(f"**{format_currency(line_total)}**")

    st.markdown("---")

    # Totals
    subtotal, discount, tax, grand_total = compute_totals()
    st.markdown(f"**Subtotal:** {format_currency(subtotal)}")
    if discount > 0:
        st.markdown(f"**Discount:** -{format_currency(discount)} ({st.session_state.valid_promo['label']})")
    st.markdown(f"**GST ({int(TAX_RATE*100)}%):** {format_currency(tax)}")
    st.markdown(f"<h3 style='color: {PRIMARY_COLOR};'>**Grand Total: {format_currency(grand_total)}**</h3>", unsafe_allow_html=True)

    # Download Buttons
    col1, col2 = st.columns(2)
    with col1:
        csv_data = make_csv()
        st.download_button(
            "📥 Download CSV",
            data=csv_data,
            file_name="invoice.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col2:
        pdf_buffer = make_pdf()
        st.download_button(
            "📄 Download PDF",
            data=pdf_buffer,
            file_name="invoice.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    if st.button("🔙 Back to Menu", use_container_width=True):
        # Order completed: clear cart and promo/payment state, then return home
        st.session_state.cart = {}
        st.session_state.promo_code = ""
        st.session_state.valid_promo = None
        st.session_state.applied_discount = Decimal("0.00")
        st.session_state.promo_qty_applied = {}
        st.session_state.payment_success = False
        st.session_state.payment_started_at = None
        st.session_state.show_invoice = False
        st.session_state.show_checkout = False
        st.rerun()

# ---------------------------
# MAIN APP
# ---------------------------

def main():
    st.set_page_config(page_title=f"{STORE_NAME} - Order Online", layout="wide", initial_sidebar_state="collapsed")

    # Custom CSS
    st.markdown(f"""
        <style>
        /* Base */
        .stApp {{
            background: {SURFACE_LIGHT};
            color: {NEUTRAL_COLOR};
        }}
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Poppins', 'Inter', sans-serif;
            color: {NEUTRAL_COLOR};
        }}
        /* Buttons - force visible text even on white backgrounds */
        .stButton > button,
        .stDownloadButton > button,
        button[kind="primary"],
        div[data-baseweb="button"] button {{
            background: {PRIMARY_COLOR} !important;
            color: #ffffff !important;
            border-radius: 50px !important;
            border: 1px solid rgba(0,0,0,0.04) !important;
            padding: 0.5rem 1rem !important;
            font-weight: 700 !important;
            text-shadow: 0 0 0 transparent !important; /* ensure no theme makes it blend */
        }}
        .stButton > button:hover,
        .stDownloadButton > button:hover,
        button[kind="primary"]:hover,
        div[data-baseweb="button"] button:hover {{
            background: {ACCENT_COLOR} !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .stButton > button:disabled,
        .stDownloadButton > button:disabled,
        button[kind="primary"][disabled] {{
            opacity: 0.6 !important;
            color: #ffffff !important;
        }}
        /* Ensure Add-ons text is clearly visible */
        div[data-testid="stExpander"] .stCheckbox label {{
            color: {NEUTRAL_COLOR} !important;
            font-weight: 500;
        }}
        div[data-testid="stExpander"] .stCheckbox span, 
        div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p {{
            color: {NEUTRAL_COLOR} !important;
        }}
        /* Expander header (Add-ons) — keep text visible even when active */
        div[data-testid="stExpander"] > details > summary {{
            background: #F3F4F6 !important; /* light gray */
            color: {NEUTRAL_COLOR} !important;
            border-radius: 8px !important;
            padding: 10px 12px !important;
            border: 1px solid #E5E7EB !important;
        }}
        div[data-testid="stExpander"] > details[open] > summary {{
            background: #EDEFF2 !important; /* slightly darker when open */
            color: {NEUTRAL_COLOR} !important;
        }}
        /* Ensure the chevron icon in the summary is also visible */
        div[data-testid="stExpander"] > details > summary svg, 
        div[data-testid="stExpander"] > details > summary svg * {{
            fill: {NEUTRAL_COLOR} !important;
            color: {NEUTRAL_COLOR} !important;
        }}
        /* Normalize control heights so Qty and Add align neatly */
        .stNumberInput > div > div > input {{
            height: 44px !important;    
            line-height: 44px !important;
        }}
        .stButton > button {{
            height: 44px !important;
            line-height: 44px !important;
        }}
        /* Slight spacing tweak so the Add button vertically centers next to the input */
        div.row-widget.stButton {{ 
            display: flex; 
            align-items: center; 
        }}
        .stNumberInput>div>div>input {{
            text-align: center;
        }}
        /* Hide sidebar */
        [data-testid="stSidebar"] {{
            display: none;
        }}
        /* Toast styling */
        .stToast {{
            background: {SECONDARY_COLOR} !important;
            color: {NEUTRAL_COLOR} !important;
        }}
        /* Ensure select dropdown renders above fixed elements */
        div[data-baseweb="select"] {{ z-index: 1000 !important; }}
        .stSelectbox {{ z-index: 1000 !important; }}
        /* Raise BaseWeb popover/menu for select widgets */
        div[data-baseweb="popover"],
        div[data-baseweb="menu"] {{ z-index: 2000 !important; }}
        /* Global bounce animation for floaters */
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-5px); }}
        }}
        .animate-bounce {{
            animation: bounce 2s infinite;
        }}
       
     
        </style>
    """, unsafe_allow_html=True)

    # Detect viewport (simplified)
    if get_query_param("viewport") == "mobile" or st.sidebar.checkbox("Mobile View", value=False):
        st.session_state["viewport"] = "mobile"
    else:
        st.session_state["viewport"] = "desktop"

    # Initialize show_checkout FIRST
    if "show_checkout" not in st.session_state:
        st.session_state.show_checkout = False
    # Then apply deep-link via query param
    if get_query_param("show_checkout") == "1":
        st.session_state.show_checkout = True

    render_header()
    render_offers_carousel()

    if not st.session_state.show_checkout:
        render_menu_grid()
        render_cart()
    else:
        if not st.session_state.cart:
            st.warning("Your cart is empty. Add some items first!")
            if st.button("🔙 Back to Menu"):
                st.session_state.show_checkout = False
                st.rerun()
        else:
            # Payment flow: show payment first, then invoice
            if not st.session_state.payment_success or not st.session_state.show_invoice:
                render_payment()
            if st.session_state.payment_success and st.session_state.show_invoice:
                render_invoice()

if __name__ == "__main__":
    main()

            # Footer
st.markdown("""
<div class="footer">
    <p><center>🎓 Keep coding, keep learning! Made with ❤️ by Shaid</center>
   
</div>
""", unsafe_allow_html=True)