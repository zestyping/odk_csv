# ODK CSV converter, a QGIS plugin

Converts CSV files from ODK Collect so they can be read directly by QGIS.

When an ODK form contains a "GeoTrace" question, ODK Collect stores the collected trace in a format that QGIS doesn't understand.  This plugin reads CSV files that were downloaded from ODK Collect and converts the GeoTrace data therein into WKT format, which QGIS can read directly.

## How to install

1. `git clone http://github.com/zestyping/odk_csv`

2. Move or copy the `odk_csv` directory created by step 1 into your QGIS application's `python/plugins` folder.  This folder is at `$HOME/.qgis2/python/plugins` on Mac/Linux and at `C:\Users\<user>\python\plugins` on Windows.

3. Restart QGIS.

4. Go to **Plugins** > **Manage and Install Plugins...** and wait a moment for the list of plugins to appear.  Type "odk" in the search box, find the "ODK CSV converter" plugin in the list, and click its check box to enable it.

## How to use

When this plugin is installed and enabled, you'll see a new "ODK -> QGIS" button on your toolbar.  Click the button, then select a CSV file that was downloaded from ODK Aggregate or KoboToolbox.  The plugin will then write out a new converted CSV file, which you can load into QGIS with the "Add Delimited Text Layer" button.

The converted file will be given a name ending in `.qgis.csv`.  For example, if the input file is named `carrots.csv`, then the converted file will be named `carrots.qgis.csv`.

## Open source license

Copyright 2017 Ka-Ping Yee

Licensed under the Apache License, Version 2.0 (the "License"); you may not
use this file except in compliance with the License.  You may obtain a copy
of the License at: http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.

