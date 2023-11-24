from common import getTrainingData, loadModel, padRms, np, os, convertNotes
from addons.sheet import extractData
import colorama, json, time, keyboard, pygetwindow, threading, re
from playsound import playsound
from termcolor import colored
from createMXL import allPitches

colorama.init()

if "usersettings.json" in os.listdir():
  with open("usersettings.json", "r") as f:
    settings = json.load(f)
    lang = settings["language"]
else:
  settings = {}
  print(colored("[!] Please choose the language. The options are:\n1) English \n2) Ukrainian \n3) Russian: ", "cyan"))
  choice = input(colored("Your choice (1, 2 or 3): ", "green"))
  if choice not in ["1", "2", "3"]:
    print(colored("\n[!!!] Invalid choice. Please try again", "red"))
    exit()
  lang = "eng" if choice == "1" else "ukr" if choice == "2" else "rus" if choice == "3" else "eng"
  settings["language"] = lang
  print(colored(("Successfully set english as the language for the interface" if lang == 'eng' else 'Успішно встановлено українську як мову для інтерфейсу' if lang == 'ukr' else 'Успешно установлено русский как язык интерфейса'), "cyan"))
  with open("usersettings.json", "w") as f:
    json.dump(settings, f, indent=2)

phrases = {
  "loadingmodels": {
    "eng": "\n[!] Loading models...",
    "ukr": "\n[!] Завантаження моделей...",
    "rus": "\n[!] Загрузка моделей..."
  },
  "modelsloaded": {
    "eng": "[!] Models loaded sucessfully\n",
    "ukr": "[!] Моделі успішно завантажені\n",
    "rus": "[!] Модели успешно загружены\n"
  },
  "inputfilename": {
    "eng": "[?] Input filename of the wav file: ",
    "ukr": "[?] Введіть ім'я файлу wav: ",
    "rus": "[?] Введите имя файла wav: "
  },
  "extractingfeatures": {
    "eng": "[!] Extracting features...",
    "ukr": "[!] Завантаження інформації...",
    "rus": "[!] Загрузка информации..."
  },
  "featuresextracted": {
    "eng": "[!] Features extracted successfully",
    "ukr": "[!] Інформацію успішно завантажено",
    "rus": "[!] Информация успешно загружена"
  },
  "predicting": {
    "eng": "\n[!] Predicting...",
    "ukr": "\n[!] Передбачення...",
    "rus": "\n[!] Предсказание..."
  },
  "predictionsdone": {
    "eng": "[!] Predicting finished successfully in {elapsed} seconds",
    "ukr": "[!] Передбачення успішно завершено за {elapsed} секунд",
    "rus": "[!] Предсказание успешно завершено за {elapsed} секунд"
  },
  "printingpredictions": {
    "eng": "\n[!] Predictions of the notes:",
    "ukr": "\n[!] Передбачення нот:",
    "rus": "\n[!] Предсказания нот:"
  },
  "editnotes": {
    "eng": "[?] Do you want to edit the notes? (y/n): ",
    "ukr": "[?] Ви хочете відредагувати ноти? (т/н): ",
    "rus": "[?] Вы хотите отредактировать ноты? (д/н): "
  },
  "tohear": {
    "eng": "[!] To hear what the note sounded in the audio press 'O'. To hear how note sounds currently press 'C'.",
    "ukr": "[!] Щоб почути, як звучала нота в аудіо, натисніть 'O'. Щоб почути, як звучить нота зараз, натисніть 'C'.",
    "rus": "[!] Чтобы услышать, как звучала нота в аудио, нажмите 'O'. Чтобы услышать, как звучит нота сейчас, нажмите 'C'."
  },
  "tonavigate": {
    "eng": "[!] To move from one note to another use the left and right arrow keys. When moving, you would hear how the note you are moving to sounds currently.",
    "ukr": "[!] Щоб перейти від однієї ноти до іншої, використовуйте клавіші зі стрілками вліво і вправо. Переміщуючись, ви будете чути, як зараз звучить нота, на яку ви переходите.",
    "rus": "[!] Чтобы перейти от одной ноты к другой, используйте стрелки влево и вправо. Перемещаясь, вы будете слышать, как сейчас звучит нота, на которую вы переходите."
  },
  "toeditpith": {
    "eng": "[!] To edit the pitch of the note use the up and down arrow keys.",
    "ukr": "[!] Щоб змінити висоту ноти, використовуйте клавіші зі стрілками вгору і вниз.",
    "rus": "[!] Чтобы изменить высоту ноты, используйте стрелки вверх и вниз."
  },
  "tofinish": {
    "eng": "[!] To finish press 'esc'.",
    "ukr": "[!] Щоб завершити натисніть 'esc'.",
    "rus": "[!] Чтобы завершить нажмите 'esc'."
  },
  "exportformat": {
    "eng": "\n[!] Please chose the export format. The options are:\n1) mxl \n2) midi ",
    "ukr": "\n[!] Будь ласка, виберіть формат експорту. Опції:\n1) mxl \n2) midi ",
    "rus": "\n[!] Пожалуйста, выберите формат экспорта. Опции:\n1) mxl \n2) midi "
  },
  "exportformatchoice": {
    "eng": "[?] Your format choice (1 or 2): ",
    "ukr": "[?] Ваш вибір (1 або 2): ",
    "rus": "[?] Ваш выбор (1 или 2): "
  },
  "savedir": {
    "eng": "\n[!] Please enter choose where to save the results. The options are:\n1) Directory of the audio file \n2) Results folder of this application \n3) Custom directory ",
    "ukr": "\n[!] Будь ласка, виберіть, куди зберегти результати. Опції:\n1) Туди ж, де знаходиться аудіо файл \n2) Папка з результатами в цій програмі \n3) Інше місце ",
    "rus": "\n[!] Пожалуйста, выберите, куда сохранить результаты. Опции:\n1) Туда же, где находится аудио файл \n2) Папка с результатами в этой программе \n3) Другое место "
  },
  "savedirchoice": {
    "eng": "[?] Your choice (1, 2 or 3): ",
    "ukr": "[?] Ваш вибір (1, 2 або 3): ",
    "rus": "[?] Ваш выбор (1, 2 или 3): "
  },
  "savedircustom": {
    "eng": "[?] Please enter the directory: ",
    "ukr": "[?] Будь ласка, введіть шлях: ",
    "rus": "[?] Пожалуйста, введите путь: "
  },
  "savingsheet": {
    "eng": "\n[!] Saving predictions as a sheet in the directory {directory}...",
    "ukr": "\n[!] Зберігання передбачень в папці {directory}...",
    "rus": "\n[!] Сохранение предсказаний в папке {directory}..."
  },
  "sheetsaved": {
    "eng": "\n[!] Data saved successfully\n",
    "ukr": "\n[!] Інформацію успішно збережено\n",
    "rus": "\n[!] Информация сохранена успешно\n"
  },

  "errors": {
    "filenotfound": {
      "eng": "[!!!] File not found. Please check the filename and try again",
      "ukr": "[!!!] Файл не знайдено. Будь ласка, перевірте назву файлу і спробуйте ще раз",
      "rus": "[!!!] Файл не найден. Пожалуйста, проверьте название файла и попробуйте еще раз"
    },
    "keyboardinterupt": {
      "eng": "\n[!] Exiting...",
      "ukr": "\n[!] Зупинка програми...",
      "rus": "\n[!] Остановка программы..."
    },
    "other": {
      "eng": "[!!!] An error {error} occured. Please !rm the developer",
      "ukr": "[!!!] Виникла помилка {error}. Будь ласка, проінформуйте розробника",
      "rus": "[!!!] Произошла ошибка {error}. Пожалуйста, проинформируйте разработчика"
    }
  }
}

def playSound(path):
  playsound(path)

def printUI():
  global newnotes, activenote
  print(colored("[!] Notes:" if lang == "eng" else "Ноти:" if lang == "ukr" else "Ноты:", "cyan"))
  print(", ".join([colored(note["visual"], "green") if i == activenote else note["visual"] for i, note in enumerate(notes)]))
  print(colored(phrases["tohear"][lang], "cyan"))
  print(colored(phrases["tonavigate"][lang], "cyan"))
  print(colored(phrases["toeditpith"][lang], "cyan"))
  print(colored(phrases["tofinish"][lang], "cyan"))

def onKeyPress(event):
  global activenote, newnotes
  activeWindow = pygetwindow.getActiveWindow().title().strip()
  if "Terminal" not in activeWindow and "Command Prompt" not in activeWindow and "Windows PowerShell" not in activeWindow and "Code" not in activeWindow: return
  try: code, name = event.scan_code, event.name
  except: code, name = None, None
  if name == "esc":
    keyboard.unhook_all()
    return
  os.system("clear")
  if code == 8:
    if "pitch" in newnotes[activenote]:
      sound_thread = threading.Thread(target=playSound, args=(f"pitchLib/note{newnotes[activenote]['pitch'].replace('#', '_')}.wav",))
      sound_thread.start()
  if code == 31: 
    if "pitch" in newnotes[activenote]:
      restsBeforeNote = len([n for n in newnotes[:activenote+1] if not "pitch" in n])
      sound_thread = threading.Thread(target=playSound, args=(f"notesTemp/note{activenote - restsBeforeNote}.wav",))
      sound_thread.start()
  elif code == 15: 
    newnotes[activenote] = notes[activenote]
  elif name == "left":
    activenote = (activenote-1)%len(notes)
    if "pitch" in newnotes[activenote]:
      sound_thread = threading.Thread(target=playSound, args=(f"pitchLib/note{newnotes[activenote]['pitch'].replace('#', '_')}.wav",))
      sound_thread.start()
  elif name == "right":
    activenote = (activenote+1)%len(notes)
    if "pitch" in newnotes[activenote]:
      sound_thread = threading.Thread(target=playSound, args=(f"pitchLib/note{newnotes[activenote]['pitch'].replace('#', '_')}.wav",))
      sound_thread.start()
  elif name == "up":
    currentPitch = allPitches.index(newnotes[activenote]["pitch"])
    currentPitch = (currentPitch+1)%len(allPitches)
    pitch = allPitches[currentPitch]
    newnotes[activenote]["pitch"] = pitch
    newnotes[activenote]["visual"] = pitch + " " + newnotes[activenote]["visual"].split(" ")[1]
    sound_thread = threading.Thread(target=playSound, args=(f"pitchLib/note{pitch.replace('#', '_')}.wav",))
    sound_thread.start()
  elif name == "down":
    currentPitch = allPitches.index(newnotes[activenote]["pitch"])
    currentPitch = (currentPitch-1)%len(allPitches)
    pitch = allPitches[currentPitch]
    newnotes[activenote]["pitch"] = pitch
    newnotes[activenote]["visual"] = pitch + " " + newnotes[activenote]["visual"].split(" ")[1]
    sound_thread = threading.Thread(target=playSound, args=(f"pitchLib/note{pitch.replace('#', '_')}.wav",))
    sound_thread.start()
  printUI()

def editNotes():
  global activenote, newnotes
  os.system("clear")
  newnotes = notes.copy()
  activenote = 0
  printUI()
  keyboard.on_press(onKeyPress)
  keyboard.wait('esc')

def main():
  global notes, newnotes
  print(colored(phrases["loadingmodels"][lang], "cyan"))

  pitchClf = loadModel("pitchClassifier")
  lengthClf = loadModel("lengthClassifierNewNew")
  restsClf = loadModel("restsClassifierAlt")

  print(colored(phrases['modelsloaded'][lang], "cyan"))

  filename = input(colored(phrases["inputfilename"][lang], "green")).split(".")[0]

  beggining = time.time()

  print(colored(phrases["extractingfeatures"][lang], "cyan"))

  try:
    X, _, _, _ = getTrainingData(filename, training=False, predicting=True, lang=lang)
  except FileNotFoundError:
    print(colored(phrases["errors"]["filenotfound"][lang], "red"))
    exit()
  except Exception as e:
    print(colored(phrases["errors"]["other"][lang].format(error=e), "red"))
    exit()

  pitchX = [([note["pitch"], np.max(note["harmonic"]), np.mean(note["harmonic"]), np.max(note["spectrogram"]), np.mean(note["spectrogram"])]) for note in X]
  lengthX = [[note["pitch"], len(note["harmonic"].flatten().tolist()), note["spectrogramLength"], note["spectrogramLength"], note["spectrogramLength"], note["spectrogramLength"]] for note in X]
  restsX = [[note["pitch"]] + padRms(note["rms"]) for note in X]

  print(colored(phrases["featuresextracted"][lang], "cyan"))
  print(colored(phrases["predicting"][lang], "cyan"))
  predictionsPitch = pitchClf.predict(pitchX)
  predictionsLength = lengthClf.predict(lengthX)
  predictionsRests = restsClf.predict(restsX)

  print(colored(phrases["predictionsdone"][lang].format(elapsed=round(time.time()-beggining, 2)), "cyan"))

  # predictionsLength = fixLengthPredictions(predictionsLength, predictionsRests)
  # print(predictionsLength)

  print(colored(phrases["printingpredictions"][lang], "cyan"))
  notes = convertNotes(predictionsPitch, predictionsLength/4, predictionsRests/4)
  print([note["visual"] for note in notes])

  choiceEditNotes = input(colored(phrases["editnotes"][lang], "green")) in ["y", "Y", "yes", "Yes", "д", "Д", "т", "Т", "да", "Да", "так", "Так"]
  newnotes = None
  if choiceEditNotes:
    editNotes()

  print(colored(phrases["exportformat"][lang], "cyan"))
  exportFormat = input(colored(phrases["exportformatchoice"][lang], "green"))
  try: exportFormat = re.findall(r'\d', exportFormat)[-1]
  except: exportFormat = "1"
  if exportFormat not in ["1", "2"]: exportFormat = "1"

  print(colored(phrases["savedir"][lang], "cyan"))
  choiceSaveDir = input(colored(phrases["savedirchoice"][lang], "green"))
  if choiceSaveDir not in ["1", "2", "3"]: choiceSaveDir = "1"
  if choiceSaveDir == "1": directory = "/".join(filename.split("/")[:-1])
  elif choiceSaveDir == "2": directory = "results"
  else: directory = input(colored(phrases["savedircustom"][lang], "green"))

  print(colored(phrases["savingsheet"][lang].format(directory=directory), "cyan"))
  os.makedirs(directory, exist_ok=True)
  extractData(predictionsPitch, predictionsLength, predictionsRests, f"{directory}/{filename.split('/')[-1]}", exportFormat=int(exportFormat), newnotes=newnotes)
  # extractData(predictionsPitch, predictionsLength, predictionsRests, f"results/{filename.split('/')[-1]}", exportFormat=int(exportFormat))
  print(colored(phrases["sheetsaved"][lang], "cyan"))

  os.system("rm -rf notesTemp")

if __name__ == "__main__":
  try: main()
  except KeyboardInterrupt: 
    print(colored(phrases["errors"]["keyboardinterupt"][lang], "red"))
    exit()