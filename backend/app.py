from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import mysql.connector
from mysql.connector import Error
from datetime import timedelta
import os
import json
from dotenv import load_dotenv

load_dotenv()

frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
UPLOAD_FOLDER = os.path.join(frontend_path, 'uploads')
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'webm', 'mov'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, static_folder=frontend_path, static_url_path='/static')
CORS(app, resources={r"/api/*": {"origins": "*"}})
bcrypt = Bcrypt(app)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
jwt = JWTManager(app)

# Database Configuration
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'adnu_mosaic')
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Database connection error: {e}")
        return None


def get_current_user():
    identity = get_jwt_identity()
    if identity == 'admin':
        return {
            'user_id': None,
            'email': 'admin@localhost',
            'full_name': 'Administrator',
            'role': 'admin'
        }

    if not identity:
        return None

    conn = get_db_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT user_id, email, full_name, role FROM users WHERE user_id = %s', (identity,))
        return cursor.fetchone()
    except Error:
        return None
    finally:
        cursor.close()
        conn.close()


def admin_required():
    user = get_current_user()
    return bool(user and user.get('role') == 'admin')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def is_video_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp4', 'webm', 'mov'}

@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400

    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Supported types are PNG, JPG, JPEG, GIF, WEBP, MP4, WEBM, MOV.'}), 400

    filename = secure_filename(file.filename)
    name, ext = os.path.splitext(filename)
    count = 1
    while os.path.exists(os.path.join(UPLOAD_FOLDER, filename)):
        filename = f"{name}-{count}{ext}"
        count += 1

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    base_url = request.host_url.rstrip('/')
    return jsonify({'url': f'{base_url}/uploads/{filename}'}), 201

# ==================== AUTHENTICATION ENDPOINTS ====================

@app.route('/api/auth/login', methods=['POST'])
def admin_login():
    """Admin login endpoint"""
    data = request.get_json()
    username = data.get('username') or data.get('email')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    # Fixed admin credentials fallback
    if username == 'admin' and password == 'admin123':
        access_token = create_access_token(identity='admin')
        return jsonify({
            'access_token': access_token,
            'user': {
                'username': 'admin',
                'role': 'admin'
            }
        }), 200

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT user_id, email, password_hash, full_name, role FROM users WHERE email = %s', (username,))
        user = cursor.fetchone()

        if not user or not bcrypt.check_password_hash(user['password_hash'], password):
            return jsonify({'error': 'Invalid credentials'}), 401

        access_token = create_access_token(identity=user['user_id'])
        return jsonify({
            'access_token': access_token,
            'user': {
                'user_id': user['user_id'],
                'email': user['email'],
                'full_name': user['full_name'],
                'role': user['role']
            }
        }), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def auth_me():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Invalid token or user not found'}), 401
    return jsonify({'user': user}), 200

@app.route('/api/auth/register', methods=['POST'])
@jwt_required()
def admin_register():
    """Admin registration (protected - requires existing admin)"""
    if not admin_required():
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')

    if not all([email, password, full_name]):
        return jsonify({'error': 'Email, password, and full name required'}), 400

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (email, password_hash, full_name, role) VALUES (%s, %s, %s, %s)',
            (email, password_hash, full_name, 'admin')
        )
        conn.commit()
        return jsonify({'message': 'Admin registered successfully'}), 201
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ==================== PINS ENDPOINTS ====================

@app.route('/api/pins', methods=['GET'])
def get_pins():
    """Get all public pins with optional filtering"""
    location_id = request.args.get('location_id', type=int)
    search = request.args.get('search', '')

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = 'SELECT * FROM pins WHERE visibility = "public"'
        params = []

        if location_id:
            query += ' AND location_id = %s'
            params.append(location_id)

        if search:
            query += ' AND (title LIKE %s OR content LIKE %s)'
            search_param = f'%{search}%'
            params.extend([search_param, search_param])

        query += ' ORDER BY created_at DESC'
        cursor.execute(query, params)
        pins = cursor.fetchall()

        # Parse image_url JSON and convert datetime objects to strings
        for pin in pins:
            if pin['created_at']:
                pin['created_at'] = pin['created_at'].isoformat()
            if pin['updated_at']:
                pin['updated_at'] = pin['updated_at'].isoformat()
            # Handle both single URL strings and JSON arrays
            if pin['image_url']:
                try:
                    # Try to parse as JSON array
                    pin['image_urls'] = json.loads(pin['image_url'])
                except (json.JSONDecodeError, TypeError):
                    # If not JSON, treat as single URL string
                    pin['image_urls'] = [pin['image_url']] if pin['image_url'] else []
            else:
                pin['image_urls'] = []
        
        return jsonify(pins), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/admin/pins', methods=['GET'])
@jwt_required()
def get_admin_pins():
    """Get all pins for admin management"""
    if not admin_required():
        return jsonify({'error': 'Admin access required'}), 403

    location_id = request.args.get('location_id', type=int)
    search = request.args.get('search', '')

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = 'SELECT * FROM pins'
        params = []

        if location_id:
            query += ' WHERE location_id = %s'
            params.append(location_id)

        if search:
            query += ' WHERE' if not params else ' AND'
            query += ' (title LIKE %s OR content LIKE %s OR author LIKE %s)'
            search_param = f'%{search}%'
            params.extend([search_param, search_param, search_param])

        query += ' ORDER BY created_at DESC'
        cursor.execute(query, params)
        pins = cursor.fetchall()

        for pin in pins:
            if pin['created_at']:
                pin['created_at'] = pin['created_at'].isoformat()
            if pin['updated_at']:
                pin['updated_at'] = pin['updated_at'].isoformat()
            if pin['image_url']:
                try:
                    pin['image_urls'] = json.loads(pin['image_url'])
                except (json.JSONDecodeError, TypeError):
                    pin['image_urls'] = [pin['image_url']] if pin['image_url'] else []
            else:
                pin['image_urls'] = []

        return jsonify(pins), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/pins/<int:pin_id>', methods=['GET'])
def get_pin(pin_id):
    """Get a single pin by ID"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM pins WHERE pin_id = %s', (pin_id,))
        pin = cursor.fetchone()

        if not pin:
            return jsonify({'error': 'Pin not found'}), 404

        if pin['created_at']:
            pin['created_at'] = pin['created_at'].isoformat()
        if pin['updated_at']:
            pin['updated_at'] = pin['updated_at'].isoformat()
        
        # Parse image_url JSON for multiple images
        if pin['image_url']:
            try:
                pin['image_urls'] = json.loads(pin['image_url'])
            except (json.JSONDecodeError, TypeError):
                pin['image_urls'] = [pin['image_url']] if pin['image_url'] else []
        else:
            pin['image_urls'] = []

        return jsonify(pin), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/pins', methods=['POST'])
def create_pin():
    """Create a new pin"""
    data = request.get_json()

    required_fields = ['title', 'content', 'author']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        # Handle both single image_url and multiple image_urls
        image_url = data.get('image_url')
        image_urls = data.get('image_urls', [])

        if image_urls and len(image_urls) > 0:
            stored_image = json.dumps(image_urls)
        elif image_url:
            stored_image = image_url
        else:
            stored_image = None

        cursor.execute(
            '''INSERT INTO pins (author, title, content, location_id, latitude, longitude, 
                                 location_name, category, visibility, image_url)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
            (
                data.get('author'),
                data.get('title'),
                data.get('content'),
                data.get('location_id'),
                data.get('latitude'),
                data.get('longitude'),
                data.get('location_name', 'Campus'),
                data.get('category', 'campus'),
                data.get('visibility', 'public'),
                stored_image
            )
        )
        conn.commit()
        pin_id = cursor.lastrowid
        return jsonify({'message': 'Pin created successfully', 'pin_id': pin_id}), 201
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/pins/<int:pin_id>', methods=['PUT'])
@jwt_required()
def update_pin(pin_id):
    """Update an existing pin (admin only)"""
    data = request.get_json()

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()

        # Build dynamic update query
        update_fields = []
        update_values = []

        for field in ['title', 'content', 'author', 'location_id', 'latitude', 'longitude', 'location_name', 'category', 'visibility', 'image_url']:
            if field in data:
                update_fields.append(f'{field} = %s')
                update_values.append(data[field])

        if 'image_urls' in data:
            update_fields.append('image_url = %s')
            update_values.append(json.dumps(data['image_urls']))

        if not update_fields:
            return jsonify({'error': 'No fields to update'}), 400

        update_values.append(pin_id)
        query = f'UPDATE pins SET {", ".join(update_fields)}, updated_at = CURRENT_TIMESTAMP WHERE pin_id = %s'

        cursor.execute(query, update_values)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': 'Pin not found'}), 404

        return jsonify({'message': 'Pin updated successfully'}), 200
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/pins/<int:pin_id>', methods=['DELETE'])
@jwt_required()
def delete_pin(pin_id):
    """Delete a pin (admin only)"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    if not admin_required():
        return jsonify({'error': 'Admin access required'}), 403

    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM pins WHERE pin_id = %s', (pin_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': 'Pin not found'}), 404

        return jsonify({'message': 'Pin deleted successfully'}), 200
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ==================== LOCATIONS ENDPOINTS ====================

@app.route('/api/locations', methods=['GET'])
def get_locations():
    """Get all campus locations"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM locations ORDER BY location_name')
        locations = cursor.fetchall()
        return jsonify(locations), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/locations/<int:location_id>', methods=['GET'])
def get_location(location_id):
    """Get a single location by ID with coordinates"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT location_id, location_name, latitude, longitude, description FROM locations WHERE location_id = %s', (location_id,))
        location = cursor.fetchone()

        if not location:
            return jsonify({'error': 'Location not found'}), 404

        return jsonify(location), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/locations', methods=['POST'])
@jwt_required()
def create_location():
    """Create a new location (admin only)"""
    if not admin_required():
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json()

    if not data.get('location_name'):
        return jsonify({'error': 'Location name required'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO locations (location_name, latitude, longitude, description)
               VALUES (%s, %s, %s, %s)''',
            (
                data.get('location_name'),
                data.get('latitude'),
                data.get('longitude'),
                data.get('description')
            )
        )
        conn.commit()
        return jsonify({'message': 'Location created successfully', 'location_id': cursor.lastrowid}), 201
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/locations/<int:location_id>', methods=['PUT'])
@jwt_required()
def update_location(location_id):
    """Update a location (admin only)"""
    if not admin_required():
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE locations SET location_name = %s, latitude = %s, longitude = %s, description = %s
               WHERE location_id = %s''',
            (
                data.get('location_name'),
                data.get('latitude'),
                data.get('longitude'),
                data.get('description'),
                location_id
            )
        )
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': 'Location not found'}), 404

        return jsonify({'message': 'Location updated successfully'}), 200
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/locations/<int:location_id>', methods=['DELETE'])
@jwt_required()
def delete_location(location_id):
    """Delete a location (admin only)"""
    if not admin_required():
        return jsonify({'error': 'Admin access required'}), 403

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM locations WHERE location_id = %s', (location_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': 'Location not found'}), 404

        return jsonify({'message': 'Location deleted successfully'}), 200
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ==================== STATS ENDPOINT ====================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get application statistics"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT COUNT(*) as total_pins FROM pins')
        total_pins = cursor.fetchone()['total_pins']

        cursor.execute('SELECT COUNT(*) as public_pins FROM pins WHERE visibility = "public"')
        public_pins = cursor.fetchone()['public_pins']

        cursor.execute('SELECT COUNT(*) as locations FROM locations')
        locations = cursor.fetchone()['locations']

        return jsonify({
            'total_pins': total_pins,
            'public_pins': public_pins,
            'locations': locations
        }), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ==================== UPLOADS / STATIC SITE ====================

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/')
@app.route('/adnu-mosaic.html')
def home():
    try:
        return send_from_directory(frontend_path, 'adnu-mosaic.html')
    except Exception as e:
        print(f"Error serving home page: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/admin')
@app.route('/admin.html')
def admin_page():
    try:
        return send_from_directory(frontend_path, 'admin.html')
    except Exception as e:
        print(f"Error serving admin page: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/map')
@app.route('/adnu-mosaic-react.html')
def map_page():
    try:
        return send_from_directory(frontend_path, 'adnu-mosaic-react.html')
    except Exception as e:
        print(f"Error serving map page: {e}")
        return jsonify({'error': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'message': 'Endpoint not found', 'success': False}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'message': 'Internal server error', 'success': False}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)