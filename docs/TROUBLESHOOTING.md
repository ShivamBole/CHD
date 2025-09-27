# 🔧 Troubleshooting Guide - "Failed to fetch" Error

## 🚨 Common Issues and Solutions

### 1. **API Server Not Running**
**Problem**: Flask API server is not started
**Solution**: 
```bash
python chd_prediction_api.py
```
**Check**: Look for "Running on http://127.0.0.1:5000" in terminal

### 2. **Port 5000 Blocked or In Use**
**Problem**: Another service is using port 5000
**Solutions**:
- Kill processes using port 5000:
  ```bash
  netstat -ano | findstr :5000
  taskkill /PID <PID_NUMBER> /F
  ```
- Use a different port by modifying the Flask app:
  ```python
  app.run(host='0.0.0.0', port=5001, debug=True)
  ```

### 3. **CORS Issues**
**Problem**: Browser blocking cross-origin requests
**Solution**: The API already has CORS configured, but if issues persist:
```python
# In chd_prediction_api.py
CORS(app, origins=['*'], methods=['GET', 'POST', 'OPTIONS'])
```

### 4. **Firewall/Antivirus Blocking**
**Problem**: Security software blocking local connections
**Solution**: 
- Add localhost:5000 to firewall exceptions
- Temporarily disable antivirus for testing

### 5. **React App Connection Issues**
**Problem**: React app can't reach the API
**Solutions**:
- Check if API is accessible: `http://localhost:5000/health`
- Try using `http://127.0.0.1:5000` instead of `localhost:5000`
- Clear browser cache and cookies

## 🧪 Testing Steps

### Step 1: Test API Directly
```bash
# Test health endpoint
curl http://localhost:5000/health

# Test prediction endpoint
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 45, "education": "2", "sex": "M", "is_smoking": "NO", "cigsPerDay": "0", "BPMeds": "NO", "prevalentStroke": "NO", "prevalentHyp": "NO", "diabetes": "NO", "totChol": 200, "sysBP": 120, "diaBP": 80, "BMI": 25.0, "heartRate": 75, "glucose": 85}'
```

### Step 2: Test React App
1. Open browser developer tools (F12)
2. Go to Network tab
3. Submit the form
4. Check for failed requests

### Step 3: Check Console Errors
Look for specific error messages in browser console:
- `ERR_CONNECTION_REFUSED`: API not running
- `CORS error`: Cross-origin issues
- `TypeError: Failed to fetch`: Network issues

## 🔄 Quick Fixes

### Fix 1: Restart Both Servers
```bash
# Stop all Python processes
taskkill /f /im python.exe

# Restart API
python chd_prediction_api.py

# In another terminal, restart React
npm start
```

### Fix 2: Use Different Ports
If port 5000 is problematic:
```python
# In chd_prediction_api.py, change:
app.run(host='0.0.0.0', port=5001, debug=True)
```
Then update React app to use `http://localhost:5001`

### Fix 3: Check Network Configuration
```bash
# Check if port is listening
netstat -an | findstr :5000

# Check if localhost resolves
ping localhost
```

## 🎯 Success Indicators

### ✅ API Working
- Terminal shows: "Running on http://127.0.0.1:5000"
- Browser shows JSON response at `http://localhost:5000/health`
- No error messages in API terminal

### ✅ React App Working
- Form submits without "Failed to fetch" error
- Results display with risk assessment
- No CORS errors in browser console

## 🆘 Still Having Issues?

1. **Check both terminals** - API and React should both be running
2. **Try different browser** - Sometimes browser extensions cause issues
3. **Disable antivirus temporarily** - Security software can block local connections
4. **Use incognito mode** - Eliminates browser cache/cookie issues
5. **Check Windows Firewall** - May be blocking localhost connections

## 📞 Quick Test Commands

```bash
# Test API health
curl http://localhost:5000/health

# Test with PowerShell
Invoke-WebRequest -Uri "http://localhost:5000/health" -Method GET

# Check if port is open
telnet localhost 5000
```

## 🔧 Advanced Debugging

### Enable Detailed Logging
Add to Flask app:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Network Requests
In browser DevTools → Network tab:
- Look for failed requests (red entries)
- Check request/response headers
- Verify CORS headers are present

### Test with Postman
Use Postman to test API endpoints directly:
- GET `http://localhost:5000/health`
- POST `http://localhost:5000/predict` with JSON body