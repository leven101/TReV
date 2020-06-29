import sys
import os
import vlc
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
import pafy

class SimplePlayer(QMainWindow):
    """
    Extremely simple video player using libVLC.
    Consists of vertical layout, widget, and a QLabel
    """

    def __init__(self, master=None):
        QMainWindow.__init__(self, master)

        # Define file variables
        url = 'https://www.youtube.com/watch?v=UPmi7TBjgYA'
        video = pafy.new(url)
        best = video.getbest()
        playurl = best.url
        self.playlist = [playurl]
        # self.playlist = ['video_file_1.mp4', 'video_file_2.mp4']

        # Define the QT-specific variables we're going to use
        self.vertical_box_layout = QVBoxLayout()
        self.central_widget = QWidget(self)
        self.video_frame = QLabel()

        # Define the VLC-specific variables we're going to use
        self.vlc_instance = vlc.Instance('--quiet')
        self.vlc_player = self.vlc_instance.media_list_player_new()
        self.media_list = self.vlc_instance.media_list_new(self.playlist)

        # Create the user interface, set up the player, and play the 2 videos
        self.create_user_interface()
        self.video_player_setup()
        self.vlc_player.play()

    def video_player_setup(self):
        """Sets media list for the VLC player and then sets VLC's output to the video frame"""
        self.vlc_player.set_media_list(self.media_list)
        self.vlc_player.get_media_player().set_nsobject(int(self.video_frame.winId()))

    def create_user_interface(self):
        """Create a 1280x720 UI consisting of a vertical layout, central widget, and QLabel"""
        self.setCentralWidget(self.central_widget)
        self.vertical_box_layout.addWidget(self.video_frame)
        self.central_widget.setLayout(self.vertical_box_layout)

        # self.resize(1280, 720)


if __name__ == '__main__':
    # app = QApplication([])
    # player = SimplePlayer()
    # player.show()
    # sys.exit(app.exec_())
    os.system('/Applications/VLC.app/Contents/MacOS/VLC https://www.youtube.com/watch?v=UPmi7TBjgYA')