# AdNU Mosaic - Campus Memory Map Application

A modern web application where Ateneo de Naga University students and faculty can share and explore campus memories pinned by location.

## Architecture Changes

This updated version includes:

✅ **Separate Pages**
- **Explore**: Browse and search campus memories with interactive map
- **Create Pin**: Form to submit new memories with location tagging
- **Admin Portal**: Secure login for administrators to manage content

✅ **Modern Frontend**
- React-based architecture with component separation
- Responsive design for mobile and desktop
- Client-side filtering and search

✅ **Enhanced Backend**
- Complete REST API with JWT authentication
- Location-based filtering
- Admin authentication and authorization
- Comprehensive error handling

✅ **Database Schema**
- Users table for admin authentication
- Locations table for campus points
- Pins table with full metadata
- Relationship constraints and indexing

## Setup Instructions

### 1. Database Setup

1. Install MySQL (if not already installed)
2. Create the database and tables:
   ```bash
   mysql -u root -p < database_schema.sql
   ```

3. Default admin account:
   - Email: `admin@adnu.edu.ph`
   - Password: `admin123` (change in production)

### 2. Backend Setup

1. Navigate to backend folder:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

5. Update `.env` with your database credentials:
   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=adnu_mosaic
   JWT_SECRET_KEY=your-super-secret-key
   ```

6. Run Flask server:
   ```bash
   python app.py
   ```
   Server runs on: `http://localhost:5000`

### 3. Frontend Setup

1. Open `adnu-mosaic-react.html` in your browser or use a local server:
   ```bash
   # Using Python
   python -m http.server 8000
   # Then visit http://localhost:8000/adnu-mosaic-react.html
   ```

   Or use VS Code Live Server extension

## API Endpoints

### Authentication
- `POST /api/auth/login` - Admin login
- `POST /api/auth/register` - Register new admin (protected)

### Pins
- `GET /api/pins` - Get all public pins
- `GET /api/pins?search=query` - Search pins
- `GET /api/pins?location_id=1` - Filter by location
- `GET /api/pins/<id>` - Get single pin
- `POST /api/pins` - Create new pin
- `PUT /api/pins/<id>` - Update pin (protected)
- `DELETE /api/pins/<id>` - Delete pin (protected)

### Locations
- `GET /api/locations` - Get all campus locations
- `POST /api/locations` - Create new location (protected)

### Statistics
- `GET /api/stats` - Get application statistics

## Frontend Features

### Explore Page
- View all campus memories on grid layout
- Search by title or story content
- Filter by location
- View memory details with author and timestamp
- Interactive map placeholder (ready for Leaflet/Mapbox integration)

### Create Pin Page
- Simple form to submit new memories
- Author name field
- Memory title and detailed story
- Location selection from campus database
- Category selection (Campus, Event, Friendship, Achievement, Other)
- Success confirmation message

### Admin Portal
- Secure login with JWT authentication
- Protected access to admin functions
- Token stored in localStorage for session persistence
- Ready for admin dashboard features (edit/delete pins, manage locations)

## Key Features

🔐 **Security**
- JWT token-based authentication
- Password hashing with bcrypt
- CORS configuration
- Protected admin endpoints

📍 **Location-Based**
- Campus location database with coordinates
- Pin filtering by location
- Ready for map API integration

🔍 **Search & Filter**
- Full-text search on titles and content
- Location-based filtering
- Client-side filtering for instant results

📱 **Responsive Design**
- Mobile-first approach
- Adaptive grid layouts
- Touch-friendly interface

## Next Steps - Map Integration

To add interactive maps (currently placeholders):

1. **Option A: Leaflet (Free, No API Key)**
   ```html
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
   <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
   ```

2. **Option B: Google Maps (Requires API Key)**
   ```html
   <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY"></script>
   ```

3. Add to the map container:
   ```javascript
   const map = L.map('map-container').setView([13.6208, 123.1846], 16);
   L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
   
   // Add markers from pins
   app.pins.forEach(pin => {
     L.marker([pin.latitude, pin.longitude])
       .bindPopup(`<strong>${pin.title}</strong><br>${pin.author}`)
       .addTo(map);
   });
   ```

## Project Structure

```
backend/
├── app.py                 # Flask application with API routes
├── requirements.txt       # Python dependencies
├── .env                   # Configuration (git-ignored)
└── .env.example          # Configuration template

frontend/
├── adnu-mosaic-react.html # Modern React-based frontend

database/
└── database_schema.sql    # MySQL database schema

README.md                  # This file
```

## Testing the Application

1. **Create a memory:**
   - Go to "Create Pin" page
   - Fill in author name, title, story
   - Select location and category
   - Click "Share Memory"

2. **View memories:**
   - Go to "Explore" page
   - Use search bar to find specific memories
   - Filter by location from dropdown
   - Click pins to view details

3. **Admin access:**
   - Go to "Admin" page
   - Login with: `admin@adnu.edu.ph` / `admin123`
   - Token persists across sessions

## Troubleshooting

### "Cannot reach server" error
- Ensure Flask is running on port 5000
- Check if MySQL is running
- Verify `.env` database credentials

### CORS errors
- Ensure frontend URL is in CORS_ORIGINS in .env
- Clear browser cache and restart

### Database connection failed
- Verify MySQL service is running
- Check username/password in .env
- Ensure database `adnu_mosaic` exists

### Pins not loading
- Check browser console for API errors
- Verify Flask server logs
- Ensure database has sample data

## Production Deployment

Before deploying:
1. Change JWT_SECRET_KEY to a strong random value
2. Update admin credentials
3. Set FLASK_ENV=production
4. Configure database for production
5. Use a production WSGI server (Gunicorn, uWSGI)
6. Enable HTTPS/SSL
7. Configure proper CORS settings
8. Set up environment variables securely

## Technologies Used

**Backend:**
- Flask 3.1.3
- Flask-CORS 4.0.0
- Flask-JWT-Extended 4.7.1
- Flask-Bcrypt 1.0.1
- MySQL Connector 8.2.0
- Python 3.8+

**Frontend:**
- React (via CDN)
- Axios for HTTP requests
- HTML5/CSS3
- Font Awesome Icons
- Playfair Display & DM Sans fonts

**Database:**
- MySQL 5.7+

## License

Educational project for Ateneo de Naga University

## Support

For issues or questions, contact the development team.
