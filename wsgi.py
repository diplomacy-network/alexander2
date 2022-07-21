# Set the path
import os, sys, app

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

app = app.app

if __name__ == "__main__":
    app.run()
