import keyboard, os, pygetwindow

# the function should check whether the terminal window is open before running the code
def on_arrow_key(event):
  # activeWindow = pygetwindow.getActiveWindow().title().strip()
  # if "Terminal" not in activeWindow and "Command Prompt" not in activeWindow and "Windows PowerShell" not in activeWindow and "Code" not in activeWindow: return
  # if event.scan_code == 31: os.system("clear"); print("O pressed")
  # elif event.scan_code == 15: os.system("clear");  print("R pressed")
  # elif event.name == "left": os.system("clear");  print("Left pressed")
  # elif event.name == "right": os.system("clear");  print("Right pressed")
  # elif event.name == "up": os.system("clear");  print("Up pressed")
  # elif event.name == "down": os.system("clear");  print("Down pressed")
  print(event.name, event.scan_code)

  # print(event.name, event.scan_code)

keyboard.on_press(on_arrow_key)

# Keep the script running
keyboard.wait()  # Wait for the 'esc' key to exit the program


# fewfwefwefwefwefwefwefwefffwefwefewf