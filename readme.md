# What can this application do?
This application can be used to make the process of transcription of an audio file with piano music much quicker and easier. It uses the power of machine learning to predict information about each note, such as its pitch, length, and information about the rests after it. It also has an interface to easily correct the pitch predictions made by the application. It allows users to then export the transcription as an mxl or midi file, which can be opened in music notation software such as MuseScore or Finale.

---

# How to install the application
First, [download the file](https://raw.githubusercontent.com/Artem4852/piano-transcription-project/main/pianoTranscriptionProject.zip) and unzip it.

Then, on Windows, open the powershell and navigate to the folder where you unzipped the file. Then, run the following command:
```batch
pip3 install -r requirements.txt
```

On Mac and Linux, open the terminal and navigate to the folder where you unzipped the file. Then, run the following command:
```zsh
pip3 install -r requirements.txt && chmod +x ./start.sh
```

The application also requires you to have [ffmpeg](https://ffmpeg.org/download.html) installed. Please use the tutorials to install it if you haven't already.

---

# Usage

## Starting the application
On Windows, open the powershell and navigate to the folder where you unzipped the file. Then, run the following command:
```batch
python3 main.py
```

On Mac, open the terminal and navigate to the folder where you unzipped the file. Then, run the following command:
```zsh
sudo ./start.sh
```

On Linux, open the terminal and navigate to the folder where you unzipped the file. Then, run the following command:
```zsh
sudo -E python3 main.py
```

## Choosing the language
When you first run the file, you would be prompted to choose the language. You can choose between English, Ukrainian and russian. To choose the language, type in the number of the language you want to choose and press enter.

## Transcribing a file
After the models are loaded, you would need to input the path to the audio file that should be transcribed.
Then, the application would split the file into notes, extract features, and predict the data about each note and rest.

## Correcting the pitch
After the transcription is done, you could choose to correct the pitch of the notes. After entering the UI, the small instructions would appear below the list of note predictions. To navigate between the notes, left/right arrow keys are used. To hear how note sounded in the file, press "O", to hear how the note sounds currectly press "C". When navigating between the notes you would also hear how the note sounds currently. This makes it very easy to see it the pitches match or not. If they don't use the up/down arrow keys to change the pitch. After you are done, press "esc" to exit the UI.

## Exporting the transcription
In the end, you can export the transcription as an mxl or midi file. You would first be prompted to enter the format you want to export the file as. Then, you would be prompted to choose where to export the file (the options are: the "results" folder of the application, the same place as the audio file is in, and custom path). If you choose the "custom path" option, you would then be prompted to enter it. After that, the file would be exported. The file would be named the same as the audio file. It could be opened in music notation software such as MuseScore or Finale.

---

# Errors
If you encounter any errors, please [create an issue](https://github.com/Artem4852/piano-transcription-project/issues/new). Please include the steps to reproduce the error, the error message, your operating system, and the version of python you are using.