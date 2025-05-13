from PyQt6 import QtWidgets, QtGui, QtCore,QtMultimedia
import sys,os

app = QtWidgets.QApplication(sys.argv)
main = QtWidgets.QMainWindow()
main.setWindowTitle("W12_4")
main.resize(600, 480)
main.setStyleSheet("background-color: #FFCCCC;")
main.setObjectName("W12_4")

playLabel = QtWidgets.QLabel(main)
playLabel.setGeometry(10, 10, 100, 30)
playLabel.setStyleSheet("background-color: #FFCCCC;")
playLabel.setText("0.0/0.0")

def PlayMusic():
    btn1.setDisabled(True)
    btn2.setDisabled(False)
    btn3.setDisabled(False)
    player.play()
    
def PauseMusic():
    btn1.setDisabled(False)
    btn2.setDisabled(True)
    btn3.setDisabled(False)
    player.pause()
    
def StopMusic():
    btn1.setDisabled(False)
    btn2.setDisabled(False)
    btn3.setDisabled(True)
    player.stop()
    
btn1 = QtWidgets.QPushButton(main)
btn1.setGeometry(10, 50, 100, 30)
btn1.setStyleSheet("background-color: #FFCCCC;")
btn1.setText("Play")
btn1.clicked.connect(PlayMusic)
btn1.setDisabled(True)

btn2 = QtWidgets.QPushButton(main)
btn2.setGeometry(10, 90, 100, 30)
btn2.setStyleSheet("background-color: #FFCCCC;")
btn2.setText("Pause")
btn2.clicked.connect(PauseMusic)

btn3 = QtWidgets.QPushButton(main)
btn3.setGeometry(10, 130, 100, 30)
btn3.setStyleSheet("background-color: #FFCCCC;")
btn3.setText("Stop")
btn3.clicked.connect(StopMusic)



playerSlider = QtWidgets.QSlider(main)
playerSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
playerSlider.setGeometry(10, 170, 580, 30)
playerSlider.setStyleSheet("background-color: #FFCCCC;")
playerSlider.setRange(0, 100)
playerSlider.setValue(0)
playerSlider.sliderMoved.connect(lambda value: player.setPosition(value))


player = QtMultimedia.QMediaPlayer(main)
path = os.getcwd() +'\\'
qurl = QtCore.QUrl.fromLocalFile(path+'kessoku band.mp3')       # 取得音樂路徑
audio_output = QtMultimedia.QAudioOutput()               # 建立音樂輸出器
player.setAudioOutput(audio_output)          # 播放器與音樂輸出器綁定
player.setSource(qurl)    # 建立音樂內容
player.durationChanged.connect(lambda duration: playerSlider.setRange(0, duration))  # 設定音樂長度
player.positionChanged.connect(lambda position: playerSlider.setValue(position))  # 設定目前播放位置
audio_output.setVolume(50)                # 設定音量
player.play()                               # 播放

def playmusic():
    progress = player.position()    # 取的目前播放時間
    playerSlider.setValue(progress)       # 設定滑桿位置
    playLabel.setText(f'{str(round(progress/1000, 1))} / {str(round(player.duration()/1000, 1))}') 

timer = QtCore.QTimer()
timer.timeout.connect(playmusic)  # 設定定時器
timer.start(100)  # 每100毫秒更新一次


# qurl = QtCore.QUrl.fromLocalFile(path + '1.mp3')
# audio_output = QtMultimedia.QAudioOutput()
# player.setAudioOutput(audio_output)
# player.setSource(qurl)
# audio_output.setVolume(50)  # 設定音 量
# player.play()  # 播放音樂

main.show()
sys.exit(app.exec())