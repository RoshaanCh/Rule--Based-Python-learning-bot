# My Python Buddy - Setup Guide

## 🚀 Quick Start (Choose One Method)

### Method 1: Windows Batch Script (Easiest)
```bash
cd "e:\python\My BUddy"
start.bat
```

### Method 2: Python Launcher (Cross-Platform)
```bash
cd "e:\python\My BUddy"
python launch.py
```

### Method 3: Manual Setup

#### Step 1: Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

#### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 3: Start Backend Server
```bash
python app.py
```

#### Step 4: Open Frontend
- Open `index.html` in your web browser directly, OR
- Start a local web server:
  ```bash
  python -m http.server 8000
  # Then visit: http://localhost:8000
  ```

## 📋 System Requirements

- **Python**: 3.8 or higher
- **Browser**: Chrome, Firefox, Safari, or Edge (latest versions)
- **RAM**: 512MB minimum
- **Disk**: 50MB free space
- **Internet**: Optional (frontend works offline after loading)

## 🔧 Configuration

### Flask Server Settings
Edit `app.py`:
```python
if __name__ == '__main__':
    app.run(
        debug=True,           # Set to False in production
        host='127.0.0.1',     # Change to 0.0.0.0 for network access
        port=5000             # Change port if 5000 is in use
    )
```

### Frontend API URL
Edit `script.js`:
```javascript
const API_URL = 'http://127.0.0.1:5000/api/chat';
```

### Customize Chatbot Responses
Edit `app.py` → `responses` dictionary:
```python
responses = {
    "your question": "your answer",
    "what is python": "Python is...",
    # Add more Q&A pairs here
}
```

### Customize Colors
Edit `style.css` → `:root` section:
```css
:root {
    --bg-primary: #0d1117;        /* Main background */
    --accent-blue: #58a6ff;       /* Primary accent */
    /* Change other colors as needed */
}
```

## 🌐 Deployment

### Local Network Access
Change in `app.py`:
```python
app.run(host='0.0.0.0', port=5000)
```
Then access from other machines using your computer's IP:
```
http://YOUR_IP:5000
```

### Production Deployment

#### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Using Docker
Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t py-buddy .
docker run -p 5000:5000 py-buddy
```

### Heroku Deployment
1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```
3. Deploy:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

## 🐛 Troubleshooting

### Issue: "Port 5000 already in use"
**Solution**: Change port in `app.py`:
```python
app.run(port=5001)  # Use different port
```
Also update `script.js`:
```javascript
const API_URL = 'http://127.0.0.1:5001/api/chat';
```

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution**: 
```bash
pip install -r requirements.txt
```

### Issue: "CORS error" in browser
**Solution**: Already configured in `app.py`. If issues persist:
```python
CORS(app, origins="*")
```

### Issue: Chatbot not responding
**Solutions**:
1. Check Flask server is running
2. Check browser console for errors (F12)
3. Verify API URL in `script.js` matches Flask server address
4. Check network tab in browser DevTools

### Issue: Styling looks broken
**Solutions**:
1. Hard refresh browser (Ctrl+F5 or Cmd+Shift+R)
2. Clear browser cache
3. Check CSS file is loaded in Network tab (F12)

## 📊 Performance Tips

1. **Minify CSS/JS** for production:
   ```bash
   pip install csscompressor jsmin
   ```

2. **Enable compression** in Flask:
   ```python
   from flask_compress import Compress
   Compress(app)
   ```

3. **Use CDN** for faster loading (optional)

4. **Enable caching** in Flask:
   ```python
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'simple'})
   ```

## 🔐 Security Checklist

- [ ] Set `debug=False` in production
- [ ] Add input validation (already implemented)
- [ ] Use HTTPS in production
- [ ] Add authentication if needed
- [ ] Rate limit API endpoints
- [ ] Sanitize all user inputs
- [ ] Use CSRF protection (Flask-WTF)
- [ ] Regular security audits

## 🎓 Learning Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **CSS Grid Guide**: https://css-tricks.com/snippets/css/complete-guide-grid/
- **Flexbox Guide**: https://css-tricks.com/snippets/css/a-guide-to-flexbox/
- **JavaScript Fetch API**: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- **Web Accessibility**: https://www.w3.org/WAI/

## 📞 Support

For issues or questions:
1. Check the README.md file
2. Review browser console errors (F12)
3. Check Flask server output for backend errors
4. Test with sample messages in DevTools console

## 📈 Future Enhancements

See README.md for planned features and improvements.

---

**Happy Learning! 🐍💙**
