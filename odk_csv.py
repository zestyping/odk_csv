from PyQt4.QtGui import QAction, QFileDialog, QIcon, QMessageBox

import csv
import os

GEOTRACE_FIELDS = ['drain_line']


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
            new_path = name + '.qgis' + ext

            conversions, errors = convert_csv(path, new_path)
            message = 'Wrote CSV output to: ' + new_path
            if errors:
                row, field = errors[0]
                line = row + 2  # row 0 is on line 2 of the file
                QMessageBox.warning(self.main, 'Warning', '''
Some problems were found and ignored.

Geotraces converted: %d
Problems found: %d
First problem: %r field on line %d

(An example of a valid geotrace field is "-6.796 39.269 27 3.2;-6.795 39.262 29 3.4".  Each point should consist of four numbers followed by a semicolon; the numbers are latitude, longitude, altitude, and accuracy.)

Fields with problems were left unchanged.  Wrote CSV output to: %s
''' % (len(conversions), len(errors), field, line, new_path))
            else:
                QMessageBox.information(self.main, 'Success', '''
All geotraces were converted successfully.

Geotraces converted: %d

Wrote CSV output to: %s
''' % (len(conversions), new_path))


def convert_csv(input_path, output_path):
    """Given the path to an input CSV file, converts the contents of all the
    fields named in GEOTRACE_FIELDS from JavaRosa format to WKT format, and
    writes a new CSV file at the given output path."""
    delimiter = detect_csv_delimiter(input_path)
    conversions, errors = [], []
    with open(input_path) as infile:
        with open(output_path, 'w') as outfile:
            reader = csv.DictReader(infile, delimiter=delimiter)
            writer = csv.DictWriter(outfile, reader.fieldnames)
            writer.writeheader()
            for r, row in enumerate(reader):
                for name in GEOTRACE_FIELDS:
                    if name in row:
                        try:
                            row[name] = convert_to_wkt(row[name])
                        except (TypeError, ValueError):
                            errors.append((r, name))
                        else:
                            conversions.append((r, name))
                writer.writerow(row)
    return conversions, errors


def convert_to_wkt(geotrace):
    """Converts a Geotrace string in JavaRosa format to a WKT LINESTRING.

    The JavaRosa format consists of points separated by semicolons, where each
    point is given as four numbers (latitude, longitude, altitude, accuracy)
    separated by spaces."""
    wkt_points = []
    for point in geotrace.split(';'):
        if point.strip():
            lat, lon, alt, accuracy = map(float, point.split())
            wkt_points.append('%.6f %.6f %d %.1f' % (lon, lat, alt, accuracy))
    return wkt_points and 'LINESTRING ZM (%s)' % (', '.join(wkt_points)) or ''


def detect_csv_delimiter(path):
    """Detects which field deliimter to use for parsing a CSV-like file."""
    # We assume that the correct delimiter is the one that causes the greatest
    # number of unique field names to be parsed from the header row.
    candidates = [(0, ',')]  # default to comma
    for delimiter in [',', '\t', ';']:
        with open(path) as infile:
            try:
                field_names = csv.reader(infile, delimiter=delimiter).next()
            except:
                continue
            candidates.append((len(set(field_names)), delimiter))
    most_fields, best_delimiter = max(candidates)
    return best_delimiter
