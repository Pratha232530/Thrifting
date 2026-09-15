import os
import base64
import tempfile
import urllib.request
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from gradio_client import Client, handle_file
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ================= DATABASE =================

client = MongoClient("mongodb://localhost:27017/")
db = client["restyle_db"]

users_collection = db["users"]
products_collection = db["products"]
orders_collection = db["orders"]

# ================= HOME =================

@app.route('/')
def home():
    return jsonify({
        "message": "RESTYLE Backend Running"
    })

# ================= REGISTER =================

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email', '').strip().lower()

    existing_user = users_collection.find_one({
        "email": email
    })

    if existing_user:
        return jsonify({
            "message": "User already exists"
        }), 400

    new_user = {
        "name": data.get('name'),
        "email": email,
        "password": generate_password_hash(data.get('password')),
        "role": "User"
    }

    users_collection.insert_one(new_user)
    
    new_user.pop("password", None)
    new_user.pop("_id", None)

    return jsonify(new_user), 201

# ================= LOGIN =================

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    user = users_collection.find_one({
        "email": email
    })

    if user and check_password_hash(user['password'], password):
        user.pop("password", None)
        user.pop("_id", None)
        return jsonify(user), 200

    return jsonify({
        "message": "Invalid credentials"
    }), 401

# ================= GET PRODUCTS =================

@app.route('/api/products', methods=['GET'])
def get_products():
    products = list(
        products_collection.find(
            {"status": "approved"},
            {"_id": 0}
        )
    )
    return jsonify(products[::-1]), 200

# ================= CREATE PRODUCT =================

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json

    if "status" not in data:
        data["status"] = "pending"

    products_collection.insert_one(data.copy())

    return jsonify({
        "message": "Product added"
    }), 201

# ================= DELETE PRODUCT =================

@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    result = products_collection.delete_one({
        "id": int(product_id)
    })

    if result.deleted_count > 0:
        return jsonify({
            "message": "Deleted"
        }), 200

    return jsonify({
        "message": "Not found"
    }), 404

# ================= PLACE ORDER =================

@app.route('/api/orders', methods=['POST'])
def place_order():
    data = request.json
    orders_collection.insert_one(data.copy())

    return jsonify({
        "message": "Order placed"
    }), 201

# ================= USER ORDERS =================

@app.route('/api/orders/<email>', methods=['GET'])
def user_orders(email):
    orders = list(
        orders_collection.find(
            {"userEmail": email},
            {"_id": 0}
        )
    )
    return jsonify(orders[::-1]), 200

# ================= ADMIN STATS =================

@app.route('/api/admin/stats', methods=['GET'])
def admin_stats():
    return jsonify({
        "products": products_collection.count_documents({}),
        "pendingProducts": products_collection.count_documents({
            "status": "pending"
        }),
        "orders": orders_collection.count_documents({}),
        "users": users_collection.count_documents({})
    })

# ================= ADMIN PRODUCTS =================

@app.route('/api/admin/products', methods=['GET'])
def admin_products():
    products = list(
        products_collection.find(
            {},
            {"_id": 0}
        )
    )
    return jsonify(products[::-1]), 200

# ================= APPROVE PRODUCT =================

@app.route('/api/admin/approve-product/<product_id>', methods=['PUT'])
def approve_product(product_id):
    result = products_collection.update_one(
        {"id": int(product_id)},
        {"$set": {"status": "approved"}}
    )

    if result.modified_count > 0:
        return jsonify({
            "message": "Approved"
        }), 200

    return jsonify({
        "message": "Not found"
    }), 404

# ================= REJECT PRODUCT =================

@app.route('/api/admin/reject-product/<product_id>', methods=['PUT'])
def reject_product(product_id):
    result = products_collection.update_one(
        {"id": int(product_id)},
        {"$set": {"status": "rejected"}}
    )

    if result.modified_count > 0:
        return jsonify({
            "message": "Rejected"
        }), 200

    return jsonify({
        "message": "Not found"
    }), 404

# ================= ADMIN USERS =================

@app.route('/api/admin/users', methods=['GET'])
def admin_users():
    users = list(
        users_collection.find(
            {},
            {
                "_id": 0,
                "password": 0
            }
        )
    )
    return jsonify(users), 200

# ================= DELETE USER =================

@app.route('/api/admin/delete-user/<email>', methods=['DELETE'])
def delete_user(email):
    result = users_collection.delete_one({
        "email": email
    })

    if result.deleted_count > 0:
        return jsonify({
            "message": "User deleted"
        }), 200

    return jsonify({
        "message": "User not found"
    }), 404

# ================= ADMIN ALL ORDERS =================

@app.route('/api/orders/all', methods=['GET'])
def all_orders():
    orders = list(
        orders_collection.find(
            {},
            {"_id": 0}
        )
    )
    return jsonify(orders[::-1]), 200

# ================= UPDATE ORDER =================

@app.route('/api/orders/update/<order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.json

    # Changed from "id" to "orderId" to match frontend generation
    result = orders_collection.update_one(
        {"orderId": order_id},
        {"$set": {"status": data.get("status")}}
    )

    if result.modified_count > 0:
        return jsonify({
            "message": "Order updated"
        }), 200

    return jsonify({
        "message": "Order not found"
    }), 404

# ================= 100% FREE AI VIRTUAL TRY-ON =================

@app.route('/api/try-on/generate', methods=['POST'])
def generate_real_tryon():
    data = request.json
    
    user_image_b64 = data.get('userImage')
    garment_image_b64 = data.get('garmentImage')

    if not user_image_b64 or not garment_image_b64:
        return jsonify({"message": "Missing images"}), 400

    try:
        print("🚀 Connecting to FREE Hugging Face AI Servers...")
        
        # 1. SMART IMAGE HANDLER: Deals with Unsplash URLs AND Webcam Selfies
        def prepare_image(img_input, prefix):
            if img_input.startswith('http'):
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg", prefix=prefix)
                urllib.request.urlretrieve(img_input, temp_file.name)
                return temp_file.name
            else:
                header, encoded = img_input.split(",", 1)
                file_ext = header.split(";")[0].split("/")[1]
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}", prefix=prefix)
                temp_file.write(base64.b64decode(encoded))
                temp_file.close()
                return temp_file.name

        user_img_path = prepare_image(user_image_b64, "user_")
        garm_img_path = prepare_image(garment_image_b64, "garm_")

        # 2. Connect to the free public IDM-VTON space
        hf_token = os.getenv("HF_TOKEN")
        client = Client("yisol/IDM-VTON", hf_token=hf_token) if hf_token else Client("yisol/IDM-VTON")
        # 3. Send the images to the free AI
        result = client.predict(
            dict={"background": handle_file(user_img_path), "layers": [], "composite": None},
            garm_img=handle_file(garm_img_path),
            garment_des="RESTYLE Thrift Garment",
            is_checked=True,
            is_checked_crop=False,
            denoise_steps=30,
            seed=42,
            api_name="/tryon"
        )
        
        # 4. Get the generated image path from the AI
        generated_img_path = result[0]
        
        # 5. Convert the resulting image back to Base64 to send to your HTML
        with open(generated_img_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            final_b64 = f"data:image/png;base64,{encoded_string}"

        # 6. Clean up the temporary files from your computer
        os.remove(user_img_path)
        os.remove(garm_img_path)

        print("✅ Free AI Generation Complete!")
        return jsonify({"generated_image_url": final_b64}), 200

    except Exception as e:
        print(f"⚠️ Free API Error: {e}")
        return jsonify({"message": "Hugging Face servers are currently busy. Try again in a minute!"}), 500

if __name__ == '__main__':
    # Runs the server on http://localhost:5000
    app.run(debug=True, port=5000)