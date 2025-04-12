import streamlit as st
import mysql.connector
from datetime import datetime
from streamlit_extras.let_it_rain import rain
from twilio.rest import Client

# ---------- Twilio Setup ----------
TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_PHONE_NUMBER = ""
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# ---------- Background Styling ----------
def set_bg():
    bg_style = """
    <style>
    .stApp { background: linear-gradient(135deg, #fff5f580, #ffd6d680); }
    body, p, div, span, input, select, textarea, button { color: white !important; }
    h1, h2, h3, h4, h5, h6 { color: #ff0000 !important; }
    h1 { font-size: 50px; font-weight: bold; text-align: center; }
    h2 { font-size: 30px; font-weight: bold; }
    p { font-size: 20px; text-align: center; color: #FAFAFA !important; }
    .interactive-card {
        background-color: #ffffff90; border-radius: 10px; padding: 20px;
        margin: 15px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease; border: 1px solid #ffcccc;
        color: #333333 !important;
    }
    .interactive-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(255, 0, 0, 0.2);
        border: 1px solid #ff0000;
    }
    .pop-button {
        background-color: #ff0000; color: white !important; border: none;
        padding: 12px 24px; font-size: 16px; border-radius: 25px;
        transition: all 0.3s ease; box-shadow: 0 4px 8px rgba(255, 0, 0, 0.2);
    }
    .pop-button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(255, 0, 0, 0.3);
        background-color: #cc0000;
    }
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)

set_bg()

# ---------- MySQL Connection ----------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Santhu@123",
    database="BloodDonationSystem"
)
cursor = conn.cursor()

# ---------- Rain Effect ----------
rain(emoji="🩸", font_size=20, falling_speed=5, animation_length=12)

# ---------- Header ----------
st.markdown("""
    <h1>🩸 Blood Donation Portal </h1>
    <p style="color:#444444;">Save lives by donating blood or finding a donor easily.</p>
""", unsafe_allow_html=True)

# ---------- Menu ----------
menu = ["🏠 Home", "📝 Register Donor", "🔎 Find Donor", "🗕️ Book Appointment", "📜 View Donations", "🆔 Generate Receipt"]
choice = st.radio("Select an option:", menu, horizontal=True)

# ---------- Home ----------
if choice == "🏠 Home":
    st.markdown("<h2>Welcome to Our Blood Donation Community</h2>", unsafe_allow_html=True)
    features = [
        {"icon": "🚑", "title": "Emergency Blood Requests", "desc": "Find urgent blood requirements in your area"},
        {"icon": "🏥", "title": "Host a Blood Drive", "desc": "Organize blood donation camps"},
        {"icon": "📢", "title": "Awareness Campaigns", "desc": "Educate about blood donation benefits"},
        {"icon": "🎖️", "title": "Donor Recognition", "desc": "Certificates for regular donors"},
        {"icon": "📱", "title": "Mobile Blood Banks", "desc": "Check our mobile collection schedule"}
    ]
    for feature in features:
        st.markdown(f"""
        <div class="interactive-card">
            <h3>{feature['icon']} {feature['title']}</h3>
            <p style="color:#444444;">{feature['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

# ---------- Register Donor ----------
elif choice == "📝 Register Donor":
    st.markdown("<h2>Register as a Blood Donor</h2>", unsafe_allow_html=True)
    with st.container():
        st.markdown("""<div class="interactive-card">""", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            blood_type = st.selectbox("Blood Type", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        with col2:
            phone = st.text_input("Phone Number")
            email = st.text_input("Email (Optional)")
            city = st.text_input("City")
        last_donation_date = st.date_input("Last Donation Date (Optional)", None)
        st.markdown("""</div>""", unsafe_allow_html=True)
        if st.button("✅ Register", key="register_btn"):
            last_donation_date = last_donation_date.strftime('%Y-%m-%d') if last_donation_date else None
            cursor.execute("""
                INSERT INTO Donors (name, blood_type, phone, email, city, last_donation_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, blood_type, phone, email, city, last_donation_date))
            donor_id = cursor.lastrowid
            donation_date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("INSERT INTO Donations (donor_id, donation_date) VALUES (%s, %s)", (donor_id, donation_date))
            conn.commit()
            st.success(f"🎉 Donor Registered Successfully! Your Donor ID is: {donor_id}")

# ---------- Find Donor ----------
elif choice == "🔎 Find Donor":
    st.markdown("<h2>Search for a Blood Donor</h2>", unsafe_allow_html=True)
    blood_type_search = st.selectbox("Select Blood Type", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    city_search = st.text_input("Enter City")
    if st.button("🔍 Find Donor"):
        cursor.execute("SELECT name, phone, email FROM Donors WHERE blood_type = %s AND city = %s", (blood_type_search, city_search))
        results = cursor.fetchall()
        if results:
            st.success(f"Found {len(results)} donor(s):")
            for name, phone, email in results:
                st.markdown(f"**Name:** {name}<br>**Phone:** {phone}<br>**Email:** {email or 'N/A'}", unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.warning("No donors found for this blood type in the specified city.")

# ---------- Book Appointment ----------
elif choice == "🗕️ Book Appointment":
    st.markdown("<h2>Schedule a Blood Donation Appointment</h2>", unsafe_allow_html=True)
    with st.container():
        st.markdown("""<div class="interactive-card">""", unsafe_allow_html=True)
        full_name = st.text_input("Full Name")
        contact = st.text_input("Contact Number (with country code e.g. +91...)")
        blood_group = st.selectbox("Blood Type", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        city = st.text_input("Enter City")
        appointment_date = st.date_input("Select Date")
        st.markdown("""</div>""", unsafe_allow_html=True)

        if st.button("🗕️ Confirm Appointment", key="appointment_btn"):
            appointment_date_str = appointment_date.strftime('%Y-%m-%d')
            cursor.execute("""
                INSERT INTO Appointment (name, contact, blood_group, city, date)
                VALUES (%s, %s, %s, %s, %s)
            """, (full_name, contact, blood_group, city, appointment_date_str))
            conn.commit()
            st.success(f"🎉 Appointment confirmed for {appointment_date_str} in {city}!")

            # Send SMS
            message_body = (
                f"Hi {full_name}, your blood donation appointment is confirmed on {appointment_date_str} in {city}. "
                f"Thank you for saving lives! ❤️🩸"
            )
            try:
                twilio_client.messages.create(
                    body=message_body,
                    from_=TWILIO_PHONE_NUMBER,
                    to=contact
                )
                st.success("📩 Confirmation SMS sent successfully!")
            except Exception as e:
                st.error(f"⚠️ SMS failed to send: {e}")

elif choice == "📜 View Donations":
    st.markdown("<h2 style='color:red;'>📋 Registered Donors</h2>", unsafe_allow_html=True)

    # Fetch donor data including DonorID
    cursor.execute("SELECT donor_id, name, blood_type, city FROM Donors")
    donors = cursor.fetchall()

    if donors:
        import pandas as pd
        import matplotlib.pyplot as plt

        # Create DataFrame
        df = pd.DataFrame(donors, columns=["DonorID", "Name", "BloodType", "City"])

        # ---- CARD DISPLAY ----
        for index, row in df.iterrows():
            with st.container():
                st.markdown(
                    f"""
                    <div style="background-color:black; padding: 15px; margin-bottom: 15px; border-radius: 10px;
                            border: 2px solid #00ff00; box-shadow: 2px 2px 8px #00ff00;">
                        <h4 style="color:#00ff00;">🩸 Donor: {row['Name']}</h4>
                        <p style="color:#000000;"><strong>🆔 Donor ID:</strong> {row['DonorID']}</p>
                        <p style="color:#000000;"><strong>🩺 Blood Type:</strong> {row['BloodType']}</p>
                        <p style="color:#000000;"><strong>📍 City:</strong> {row['City']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("<hr style='margin-top:40px;margin-bottom:20px;'>", unsafe_allow_html=True)

        # ---- VISUALIZATION SECTION ----
        st.markdown("<h3>📊 Donor Demographics</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        # 1. Scatter Plot - Top 10 City-wise Donor Distribution (with integer y-axis)
        with col1:
            st.subheader("🏙️ City-wise Donor Distribution (Top 10)")
            city_counts = df["City"].value_counts().head(10).reset_index()
            city_counts.columns = ["City", "Count"]

            fig1, ax1 = plt.subplots(figsize=(10, 6))
            ax1.scatter(city_counts["City"], city_counts["Count"], color='green', s=150, edgecolors='black')
            
            # Set integer scaling for y-axis
            max_count = city_counts["Count"].max()
            ax1.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
            ax1.set_ylim(0, max_count + 1)  # Add small buffer
            
            ax1.set_xlabel("City")
            ax1.set_ylabel("Number of Donors")
            ax1.set_title("🗺️ Top 10 Donors by City")
            plt.xticks(rotation=45, fontsize=10)
            plt.tight_layout()
            st.pyplot(fig1)

        # 2. Bar Chart - Blood Type Frequency (with integer y-axis)
        with col2:
            st.subheader("Blood Type Distribution")
            blood_counts = df["BloodType"].value_counts().sort_index()

            fig2, ax2 = plt.subplots()
            ax2.bar(blood_counts.index, blood_counts.values, color="#e60000", edgecolor='black')
            
            # Set integer scaling for y-axis
            max_blood = blood_counts.max()
            ax2.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
            ax2.set_ylim(0, max_blood + 1)  # Add small buffer
            
            ax2.set_xlabel("Blood Type")
            ax2.set_ylabel("Number of Donors")
            ax2.set_title("🩸 Blood Type Frequency")
            st.pyplot(fig2)

    else:
        st.warning("No donor records found.")

# ---------- Generate Receipt ----------
elif choice == "🆔 Generate Receipt":
    st.markdown("<h2>Generate Donation Receipt</h2>", unsafe_allow_html=True)
    donor_id = st.number_input("Enter Donor ID", min_value=1)
    if st.button("📄 Generate Receipt"):
        cursor.execute("SELECT D.name, D.blood_type, D.city, N.donation_date FROM Donors D JOIN Donations N ON D.donor_id = N.donor_id WHERE D.donor_id = %s", (donor_id,))
        receipt = cursor.fetchone()
        if receipt:
            name, blood, city, date = receipt
            receipt_id = f"BLD-{donor_id:05d}"
            
            # Create the receipt content
            receipt_content = f"""
            BLOOD DONATION RECEIPT
            --------------------------
            Donor Name: {name}
            Blood Group: {blood}
            City: {city}
            Donation Date: {date}
            Receipt ID: {receipt_id}
            --------------------------
            Thank you for your life-saving donation!
            """
            
            # Display the receipt
            st.markdown(f"""
            ### 📄 Donation Receipt
            - **Donor Name:** {name}
            - **Blood Group:** {blood}
            - **City:** {city}
            - **Donation Date:** {date}
            - **Receipt ID:** {receipt_id}
            """)
            
            # Create download button
            st.download_button(
                label="⬇️ Download Receipt as TXT",
                data=receipt_content,
                file_name=f"BloodDonationReceipt_{receipt_id}.txt",
                mime="text/plain",
                help="Click to download your donation receipt"
            )
        else:
            st.error("No donation record found for this Donor ID.")
# ---------- Cleanup ----------
cursor.close()
conn.close()
