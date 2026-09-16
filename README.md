# 🛍️ RESTYLE - Sustainable Fashion & AI Virtual Try-On Marketplace

![RESTYLE Banner](https://img.shields.io/badge/RESTYLE-Thrift%20%26%20Fashion-brightgreen?style=for-the-badge)
![Flask](https://img.shields.io/badge/Backend-Flask-blue?style=for-the-badge&logo=flask)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-green?style=for-the-badge&logo=mongodb)
![AI Powered](https://img.shields.io/badge/AI-HuggingFace%20IDM--VTON-orange?style=for-the-badge&logo=huggingface)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

**RESTYLE** is a full-stack sustainable fashion marketplace and thrifting web application integrated with **100% Free AI Virtual Try-On**. Users can browse curated second-hand items, sell pre-loved clothing, test items on their uploaded photo using AI, place orders, and track purchases. Admin tools allow platform managers to moderate products, manage users, and track order fulfillment.

---

## ✨ Features

- **👗 Sustainable Marketplace**: Browse, filter, and purchase pre-loved and vintage clothing.
- **🤖 Free AI Virtual Try-On**: Powered by Hugging Face's `yisol/IDM-VTON` model via Gradio Client. Users upload their photo and instantly preview how a clothing item fits.
- **🔐 User Authentication**: Secure registration and login with password hashing (`werkzeug.security`).
- **🛒 Cart & Order Management**: Shopping cart workflow, multi-payment support, and real-time user order tracking.
- **📦 Seller Portal**: List pre-loved items with image upload previews, pricing, category selection, and condition tagging.
- **🛡️ Admin Dashboard**: Moderate product listings (approve/reject), manage user accounts, review platform analytics, and update order statuses.
- **📱 Modern Responsive UI**: Glassmorphism aesthetic with responsive layouts, smooth micro-interactions, and dark mode design.

---

## 🛠️ Tech Stack

### **Backend**
- **Framework**: Python 3.x with Flask & Flask-CORS
- **Database**: MongoDB (via `pymongo`)
- **AI Integration**: Gradio Client (`gradio_client`), Hugging Face Inference Space (`yisol/IDM-VTON`)
- **PHP Integration**: `process_tryon.php`, `try_on_api.php` scripts for PHP environment bridging

### **Frontend**
- **Core**: HTML5, CSS3 (Custom Glassmorphism Utilities), Vanilla JavaScript (ES6+)
- **UI & Typography**: FontAwesome 6, Google Fonts (Plus Jakarta Sans, Inter)

---

## 📁 Project Structure

```
Thrifting/
├── app.py                 # Flask REST API Backend & AI Try-On service engine
├── index.html             # Client Marketplace Single-Page Application
├── admin.html             # Admin Management Dashboard
├── process_tryon.php      # PHP proxy script for AI Try-On endpoint
├── try_on_api.php         # PHP bridge script for local/remote try-on calls
├── .env                   # Environment config (HF_TOKEN, etc.)
├── .gitignore             # Git ignore patterns
└── README.md              # Project documentation
```

---

## ⚙️ Prerequisites & Installation

### 1. Requirements
- **Python**: 3.8 or higher
- **MongoDB**: Local MongoDB server running on `mongodb://localhost:27017/` (or MongoDB Atlas URI)
- **Hugging Face Token** *(Optional)*: HF token for higher rate limits on AI Try-On inference.

### 2. Environment Setup
Clone the repository and navigate into the project directory:
```bash
git clone https://github.com/Pratha232530/Thrifting.git
cd Thrifting
```

Create and activate a Python virtual environment:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

Install Python dependencies:
```bash
pip install flask flask-cors pymongo werkzeug gradio_client python-dotenv
```

### 3. Environment Configuration
Set up your `.env` file in the root directory:
```env
HF_TOKEN=your_huggingface_access_token_here
```

---

## 🚀 Running the Application

### 1. Start MongoDB
Ensure your MongoDB daemon is running:
```bash
mongod
```

### 2. Start Flask Backend Server
```bash
python app.py
```
The server will start at `http://localhost:5000`.

### 3. Launch Frontend
Open `index.html` in your web browser or use a live development server.
- **Client App**: `index.html`
- **Admin Dashboard**: `admin.html`

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register` | Register a new user |
| `POST` | `/api/auth/login` | Authenticate user credentials |
| `GET` | `/api/products` | Retrieve approved products catalog |
| `POST` | `/api/products` | Submit new item for review |
| `DELETE` | `/api/products/<product_id>` | Delete product listing |
| `POST` | `/api/orders` | Place a new customer order |
| `GET` | `/api/orders/<email>` | Fetch order history for user |
| `GET` | `/api/orders/all` | Retrieve all orders (Admin) |
| `PUT` | `/api/orders/update/<order_id>` | Update order status (Admin) |
| `GET` | `/api/admin/stats` | Get platform overview statistics |
| `GET` | `/api/admin/products` | Fetch all products including pending/rejected |
| `PUT` | `/api/admin/approve-product/<id>` | Approve pending listing |
| `PUT` | `/api/admin/reject-product/<id>` | Reject pending listing |
| `GET` | `/api/admin/users` | List registered users |
| `DELETE` | `/api/admin/delete-user/<email>` | Delete user account |
| `POST` | `/api/try-on/generate` | Generate AI Virtual Try-On image |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.

1. Fork the Repository
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
