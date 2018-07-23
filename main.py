from PyQt5 import QtWidgets
from pytube import YouTube
import sys
import design
import re

yt_regex = re.compile("^(http(s)??://)?(www\.)?((youtube\.com/watch\?v=)|(youtu.be/))([a-zA-Z0-9\-_])+$")
ytid_regex = re.compile("^[a-zA-Z0-9_-]{6,11}$")


class YTDownloader(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self, parent=None):
        super(YTDownloader, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(751, 260)
        self.alert = QtWidgets.QMessageBox()
        self.progress_dialog: QtWidgets.QProgressDialog = None
        self.btn_download.clicked.connect(self.download)
        self.cb_resolution.addItems(["1080p", "720p", "480p", "360p", "240p", "166p"])
        self.cb_type.addItems(["video", "audio"])
        self.cb_extension.addItems(["mp4", "webm"])

    def download(self):
        url = self.txt_yt.text()
        download = self.cb_type.currentText()
        quality = self.cb_resolution.currentText()
        file_ext = self.cb_extension.currentText()

        if url is None or url == "":
            self.show_alert(QtWidgets.QMessageBox.Critical, "Video url or id is required", QtWidgets.QMessageBox.Ok)
            return
        elif download is None or download == "":
            self.show_alert(QtWidgets.QMessageBox.Critical, "Download type is required", QtWidgets.QMessageBox.Ok)
            return
        elif quality is None or quality == "":
            self.show_alert(QtWidgets.QMessageBox.Critical, "Video resolution is required", QtWidgets.QMessageBox.Ok)
            return
        elif file_ext is None or file_ext == "":
            self.show_alert(QtWidgets.QMessageBox.Critical, "Extension type is required", QtWidgets.QMessageBox.Ok)
            return

        if yt_regex.match(url) is not None:
            link = YouTube(url)
        elif ytid_regex.match(url) is not None:
            link = YouTube("https://www.youtube.com/watch?v=" + url)
        else:
            self.show_alert(QtWidgets.QMessageBox.Critical, "Invalid input", QtWidgets.QMessageBox.Ok)
            return

        link.register_on_complete_callback(self.on_complete)
        link.register_on_progress_callback(self.show_progress_bar)

        savedir = self.open_dir_dialog()

        self.progress_dialog = QtWidgets.QProgressDialog(labelText="Downloading...", minimum=0)
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.setValue(0)
        if download == "audio":
            download_audio = link.streams.filter(subtype=file_ext, res=quality, only_audio=True).first()
            if download_audio is None:
                self.show_alert(QtWidgets.QMessageBox.Critical, "No videos found", QtWidgets.QMessageBox.Ok)
                return
            self.progress_dialog.setMaximum(download_audio.filesize)
            self.progress_dialog.open()
            download_audio.download(savedir.path())
        else:
            download_video = link.streams.filter(subtype=file_ext, res=quality).first()
            if download_video is None:
                self.show_alert(QtWidgets.QMessageBox.Critical, "No videos found", QtWidgets.QMessageBox.Ok)
                return
            self.progress_dialog.setMaximum(download_video.filesize)
            self.progress_dialog.open()
            download_video.download(savedir.path())

    def show_progress_bar(self, _stream, _chunk, _file_handle, bytes_remaining):
        progress = self.progress_dialog.maximum() - bytes_remaining
        self.progress_dialog.setValue(progress)

    def on_complete(self, _stream, _file_handle):
        self.show_alert(QtWidgets.QMessageBox.NoIcon, "Completed", QtWidgets.QMessageBox.Ok)

    def show_alert(self,
                   icon: QtWidgets.QMessageBox.Icon,
                   text: str,
                   btns: QtWidgets.QMessageBox.StandardButtons or QtWidgets.QMessageBox.StandardButton,
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
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        return QtWidgets.QFileDialog.getExistingDirectoryUrl(self, options=options, caption="Select directory")


def main():
    app = QtWidgets.QApplication(sys.argv)
    form_main = YTDownloader()
    form_main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
