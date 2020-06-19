from app import app

app.run(debug = True, host = '127.0.0.1', port = 5000)
# Production
app.run(host='0.0.0.0') 
