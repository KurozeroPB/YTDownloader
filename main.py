from PyQt5 import QtWidgets
from pytube import YouTube, Playlist
import sys
import design
import re

# Simple regex to check the users input
yt_regex = re.compile("^(http(s)??://)?(www\.)?((youtube\.com/watch\?v=)|(youtu.be/))([a-zA-Z0-9\-_])+$")
ytid_regex = re.compile("^[a-zA-Z0-9_-]{6,11}$")
playlist_regex = re.compile("^.*(youtu.be/|(list=|v=))([^#&?]*).*")


class YTDownloader(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self, parent=None):
        super(YTDownloader, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(751, 260)
        self.alert = QtWidgets.QMessageBox()
        self.progress_dialog: QtWidgets.QProgressDialog = None
        self.btn_download.clicked.connect(self.download)
        self.btn_test.clicked.connect(self.test)
        self.cb_resolution.addItems(["1080p", "720p", "480p", "360p", "240p", "166p"])
        self.cb_type.addItems(["video", "audio", "playlist"])
        self.cb_type.currentIndexChanged.connect(self.change_extensions)
        self.cb_extension.addItems(["mp4", "webm"])
        # self.txt_yt.setText("https://www.youtube.com/playlist?list=PLGZBd7o0HqUriCk_JbGXr_oHNDwFSj-8D")
        self.btn_test.setEnabled(False)
        self.btn_test.setHidden(True)

    def download(self):
        self.setEnabled(False)  # Disable main window

        url = self.txt_yt.text()
        download = self.cb_type.currentText()
        quality = self.cb_resolution.currentText()
        file_ext = self.cb_extension.currentText()

        # Check for None or empty string values
        if url is None or url == "":
            self.show_alert(QtWidgets.QMessageBox.Critical, "Video url or id is required", QtWidgets.QMessageBox.Ok)
            self.setEnabled(True)
            return
        elif download is None or download == "":
            self.show_alert(QtWidgets.QMessageBox.Critical, "Download type is required", QtWidgets.QMessageBox.Ok)
            self.setEnabled(True)
            return
        elif quality is None or quality == "":
            self.show_alert(QtWidgets.QMessageBox.Critical, "Video resolution is required", QtWidgets.QMessageBox.Ok)
            self.setEnabled(True)
            return
        elif file_ext is None or file_ext == "":
            self.show_alert(QtWidgets.QMessageBox.Critical, "Extension type is required", QtWidgets.QMessageBox.Ok)
            self.setEnabled(True)
            return

        # Make sure the input is either a youtube url or a video id
        if yt_regex.match(url) is not None:
            link = YouTube(url)
        elif ytid_regex.match(url) is not None:
            link = YouTube("https://www.youtube.com/watch?v=" + url)
        elif playlist_regex.match(url):
            self.show_alert(QtWidgets.QMessageBox.Information, "Downloading playlists is still a work in progress", QtWidgets.QMessageBox.Ok)
            self.setEnabled(True)
            return
        else:
            self.show_alert(QtWidgets.QMessageBox.Critical, "Invalid input", QtWidgets.QMessageBox.Ok)
            self.setEnabled(True)
            return

        # Register callbacks for progress bar
        link.register_on_complete_callback(self.on_complete)
        link.register_on_progress_callback(self.show_progress_bar)

        # Get the direcory where the file needs to be saved
        savedir = self.open_dir_dialog()

        # Either on cancel or close
        if savedir.toString() == "":
            self.setEnabled(True)
            return

        if download == "audio":
            # Find only audio streams
            download_audio = link.streams.filter(audio_codec=file_ext, only_audio=True).first()
            if download_audio is None:
                self.show_alert(QtWidgets.QMessageBox.Critical, "No audio found", QtWidgets.QMessageBox.Ok)
                self.setEnabled(True)
                return
            # Make progress dialog
            self.progress_dialog = QtWidgets.QProgressDialog(labelText="Downloading...", minimum=0, maximum=download_audio.filesize)
            self.progress_dialog.setAutoClose(True)
            self.progress_dialog.setValue(0)
            self.progress_dialog.open()
            # Download file to given path
            download_audio.download(savedir.path())
        elif download == "video":
            # Find only video streams
            download_video = link.streams.filter(subtype=file_ext, res=quality).first()
            if download_video is None:
                self.show_alert(QtWidgets.QMessageBox.Critical, "No videos found", QtWidgets.QMessageBox.Ok)
                self.setEnabled(True)
                return
            # Make progress dialog
            self.progress_dialog = QtWidgets.QProgressDialog(labelText="Downloading...", minimum=0, maximum=download_video.filesize)
            self.progress_dialog.setAutoClose(True)
            self.progress_dialog.setValue(0)
            self.progress_dialog.open()
            # Download file to given path
            download_video.download(savedir.path())
        elif download == "playlist":
            self.show_alert(QtWidgets.QMessageBox.Information, "Downloading playlists is still a work in progress", QtWidgets.QMessageBox.Ok)
            self.setEnabled(True)

    def show_progress_bar(self, _stream, _chunk, _file_handle, bytes_remaining):
        # Update progress bar
        progress = self.progress_dialog.maximum() - bytes_remaining
        self.progress_dialog.setValue(progress)

    def on_complete(self, _stream, _file_handle):
        self.show_alert(QtWidgets.QMessageBox.Information, "Completed", QtWidgets.QMessageBox.Ok)
        self.setEnabled(True)

    def show_alert(self,
                   icon: QtWidgets.QMessageBox.Icon,
                   text: str,
                   btns: QtWidgets.QMessageBox.StandardButton,
                   info: str = "",
                   title: str = "",
                   def_btn: QtWidgets.QMessageBox.StandardButton = None,
                   return_val: bool = False):
        self.alert.setIcon(icon)
        self.alert.setText(text)
        self.alert.setInformativeText(info)
        self.alert.setWindowTitle(title)
        self.alert.setStandardButtons(btns)
        self.alert.setDefaultButton(def_btn)
        if return_val:
            return self.alert.exec()
        else:
            self.alert.exec_()

    def open_dir_dialog(self):
        options = QtWidgets.QFileDialog.Options(QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontUseNativeDialog)
        return QtWidgets.QFileDialog.getExistingDirectoryUrl(self, options=options, caption="Select directory")

    def change_extensions(self):
        self.cb_extension.clear()
        if self.cb_type.currentText() == "video" or self.cb_type.currentText() == "playlist":
            self.lbl_extension.setText("Video extension")
            self.cb_resolution.setEnabled(True)
            self.cb_extension.addItems(["mp4", "webm"])
        elif self.cb_type.currentText() == "audio":
            self.lbl_extension.setText("Audio codec")
            self.cb_resolution.setEnabled(False)
            self.cb_extension.addItems(["opus", "vorbis", "mp4a.40.2"])

    def test(self):
        """ TODO:
        - Experimental playlist
        - Playlist option to combobox type
        - Playlist regex check
        -==========================================================================-
        Currently no way of checking whether it's complete and what the progress is,
        Possible way to loop over all url so we can get the remaining and progress
        playlist.populate_video_urls()
        playlist.video_urls
        """
        playlist_url = self.txt_yt.text()
        if playlist_url is None or playlist_url == "":
            print("Empty playlist url")
            return

        if playlist_regex.match(playlist_url):
            savedir = self.open_dir_dialog()
            if savedir.toString() == "":
                print("Canceled/closed choosing directory")
                return

            playlist = Playlist(playlist_url)
            # download_all() defaults to highest res so not optimal
            # No options or configs are available at this time
            playlist.download_all(savedir.path())
        else:
            print("No matching playlist url")


def main():
    app = QtWidgets.QApplication(sys.argv)
    form_main = YTDownloader()
    form_main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
