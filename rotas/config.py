import pyrebase

# Configuração do Firebase
config = {
    "apiKey": "AIzaSyC35Nx5PlqGFdGlx7OF-Hhks1pEQKAkoN8",
    "authDomain": "investidorprivate.firebaseapp.com",
    "databaseURL": "https://investidorprivate-default-rtdb.firebaseio.com",
    "projectId": "investidorprivate",
    "storageBucket": "investidorprivate.appspot.com",
    "messagingSenderId": "663117534406",
    "appId": "1:663117534406:web:489dd4ca3d2572b13e33c7",
    "measurementId": "G-2JSVE5BSMQ"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()