# 🩸 Blood Donation Portal

A Streamlit-based web application for registering blood donors, finding donors by city and blood group, booking donation appointments with Twilio SMS confirmation, and visualizing donor statistics with beautiful charts and interactive cards.

---

## 🚀 Features

- ✅ Donor Registration
- 🔍 Find Donors by Blood Group & City
- 📆 Book Appointment with SMS Confirmation (Twilio)
- 📊 Donor Stats Visualization (Scatter & Bar charts)
- 📋 View All Donors
- 🧾 Generate and Download Donation Receipt

---

## 📸 Screenshots

![Image 2025-04-12 at 4 53 40 PM](https://github.com/user-attachments/assets/48dee873-7b33-483e-8bf6-108b7e5a3cde)


---

## 🛠 Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Backend:** Python, MySQL
- **SMS Integration:** Twilio API
- **Data Viz:** Matplotlib, Pandas

---

## 📦 Database Structure

```sql
CREATE TABLE Donors (
    donor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    blood_type VARCHAR(5),
    phone VARCHAR(15),
    email VARCHAR(100),
    city VARCHAR(50),
    last_donation_date DATE
);

CREATE TABLE Donations (
    donation_id INT AUTO_INCREMENT PRIMARY KEY,
    donor_id INT,
    donation_date DATE,
    FOREIGN KEY (donor_id) REFERENCES Donors(donor_id)
);

CREATE TABLE Appointment (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    contact VARCHAR(20),
    blood_group VARCHAR(5),
    city VARCHAR(50),
    date DATE
);


```
``` How to Run
# Clone the repository
git clone https://github.com/Santhu7718/Blood-donation-portal.git
cd Blood-donation-portal

# Activate virtual environment (optional)
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```
```🧪 Twilio Setup
TWILIO_ACCOUNT_SID = "your_sid"
TWILIO_AUTH_TOKEN = "your_token"
TWILIO_PHONE_NUMBER = "+1..."
```

 

