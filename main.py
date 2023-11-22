from common import getTrainingData, loadModel, padRms, np, os, convertNotes
from addons.sheet import extractData
import colorama, json, time
from termcolor import colored

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
    print(colored("\n[!!!] Invalid choice. Please try again", "orange"))
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
    "eng": "\n[!] Predicting finished successfully in {elapsed} seconds}",
    "ukr": "\n[!] Передбачення успішно завершено за {elapsed} секунд",
    "rus": "\n[!] Предсказание успешно завершено за {elapsed} секунд"
  },
  "printingpredictions": {
    "eng": "\n[!] Predictions of the notes:",
    "ukr": "\n[!] Передбачення нот:",
    "rus": "\n[!] Предсказания нот:"
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

def main():
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
    print(colored(phrases["errors"]["filenotfound"][lang], "orange"))
    exit()
  except Exception as e:
    print(colored(phrases["errors"]["other"][lang].format(error=e), "orange"))
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
  print(notes)

  print(colored(phrases["exportformat"][lang], "cyan"))
  exportFormat = input(colored(phrases["exportformatchoice"][lang], "green"))
  if exportFormat not in ["1", "2"]: exportFormat = "1"

  print(exportFormat)

  print(colored(phrases["savingsheet"][lang].format(directory="results"), "cyan"))
  os.makedirs("results", exist_ok=True)
  extractData(predictionsPitch, predictionsLength, predictionsRests, f"results/{filename.split('/')[-1]}", exportFormat=int(exportFormat))
  print(colored(phrases["sheetsaved"][lang], "cyan"))

if __name__ == "__main__":
  try: main()
  except KeyboardInterrupt: 
    print(colored(phrases["errors"]["keyboardinterupt"][lang], "orange"))
    exit()