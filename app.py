# Referenced from the directory "APP" and the variable "APP" in the __init__.py file
from app import app



# Runs the application
if __name__ == "__main__":
    app.run(debug= True)