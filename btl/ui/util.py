import os
from PySide import QtCore, QtGui, QtUiTools, QtSvg

def load_ui(ui_path, parent=None, custom_widgets=None):
    loader = QtUiTools.QUiLoader(parent)
    loader.setWorkingDirectory(os.path.dirname(__file__))
    if custom_widgets:
        for widget in custom_widgets:
            loader.registerCustomWidget(widget)
    ui_file = QtCore.QFile(ui_path)
    ui_file.open(QtCore.QFile.ReadOnly)
    form = loader.load(ui_file)
    ui_file.close()
    return form

def qpixmap_from_png(byte_array, icon_size, ratio=1.0):
    render_size = QtCore.QSize(icon_size.width()*ratio, icon_size.height()*ratio)
    pixmap = QtGui.QPixmap(render_size)
    pixmap.fill(QtGui.Qt.transparent)
    pixmap.loadFromData(byte_array)
    return pixmap.scaled(icon_size, QtCore.Qt.KeepAspectRatio)

def qpixmap_from_svg(byte_array, icon_size, ratio=1.0):
    render_size = QtCore.QSize(icon_size.width()*ratio, icon_size.height()*ratio)

    image = QtGui.QImage(render_size, QtGui.QImage.Format_ARGB32)
    image.fill(QtGui.Qt.transparent)
    painter = QtGui.QPainter(image)

    data = QtCore.QXmlStreamReader(byte_array)
    renderer = QtSvg.QSvgRenderer(data)
    renderer.setAspectRatioMode(QtCore.Qt.KeepAspectRatio)
    renderer.render(painter)
    painter.end()

    return QtGui.QPixmap.fromImage(image)

def get_pixmap_from_shape(shape, size, ratio):
    icon_type, icon_bytes = shape.get_icon()
    if not icon_type:
        return None
    icon_ba = QtCore.QByteArray(icon_bytes)

    if icon_type == 'svg':
        return qpixmap_from_svg(icon_ba, size, ratio)
    elif icon_type == 'png':
        return qpixmap_from_png(icon_ba, size, ratio)

    return None
