from PyQt4.QtGui import QAction, QFileDialog, QIcon, QMessageBox
from qgis.core import QgsMessageLog

import csv
import os

GEO_FIELDS = ['drain_line']


class OdkCsvConverter(object):
    def __init__(self, iface):
        self.iface = iface
        self.main = iface.mainWindow()
        self.last_dir = os.path.expanduser('~')

    def initGui(self):
        self.action = QAction(
            QIcon(os.path.dirname(__file__) + '/button.png'),
            'Convert CSV files from ODK Collect', self.main
        )
        self.action.setStatusTip('Convert CSV files from ODK Collect')
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        self.action.triggered.disconnect(self.run)

    def run(self):
        path = QFileDialog.getOpenFileName(
            self.main, 'Select a CSV file of ODK data', self.last_dir)
        if path:
            dir, name = os.path.split(path)
            self.last_dir = dir
            name, ext = os.path.splitext(path)
            new_path = name + '-qgis' + ext

            convert_csv(path, new_path)
            QMessageBox.information(
                self.main, 'Wrote CSV', 'Wrote CSV output to: %s' % new_path)


def convert_csv(input_path, output_path):
    # KoboToolbox exports "CSV" files with semicolons as delimiters instead
    # of commas; we detect the delimiter by examining the header row.
    with open(input_path) as infile:
        comma_fields = csv.reader(infile, delimiter=',').next()
    with open(input_path) as infile:
        semicolon_fields = csv.reader(infile, delimiter=';').next()
    delimiter = (len(semicolon_fields) > len(comma_fields)) and ';' or ','

    with open(input_path) as infile:
        with open(output_path, 'w') as outfile:
            reader = csv.DictReader(infile, delimiter=delimiter)
            writer = csv.DictWriter(outfile, reader.fieldnames)
            writer.writeheader()
            for row in reader:
                for name in GEO_FIELDS:
                    if name in row:
                        row[name] = convert_to_wkt(row[name])
                writer.writerow(row)


def convert_to_wkt(geotrace):
    wkt_points = []
    for point in geotrace.split(';'):
        if point.strip():
            lat, lon, alt, accuracy = map(float, point.split())
            wkt_points.append('%.6f %.6f %.0f %.1f' % (lon, lat, alt, accuracy))
    if wkt_points:
        return 'LINESTRING ZM(%s)' % (', '.join(wkt_points))
    return ''
