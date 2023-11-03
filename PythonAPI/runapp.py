
import subprocess

def run_main():
    try:
        # use subprocess to run main.py
        subprocess.run(['python', 'PythonAPI\main.py'])
    except Exception as e:
        print(f"Error running main.py: {e}")

if __name__ == "__main__":
    run_main()

