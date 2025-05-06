from PyQt6 import QtWidgets, QtGui, QtCore,QtMultimedia
import sys,os

app = QtWidgets.QApplication(sys.argv)
main = QtWidgets.QMainWindow()
main.setWindowTitle("W12_4")
main.resize(600, 480)
main.setStyleSheet("background-color: #FFCCCC;")
main.setObjectName("W12_4")

player = QtMultimedia.QMediaPlayer(main)
path = os.getcwd() +'\\'
print(path)

# qurl = QtCore.QUrl.fromLocalFile(path + '1.mp3')
# audio_output = QtMultimedia.QAudioOutput()
# player.setAudioOutput(audio_output)
# player.setSource(qurl)
# audio_output.setVolume(50)  # 設定音量
# player.play()  # 播放音樂

main.show()
sys.exit(app.exec())