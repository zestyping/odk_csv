# ODK CSV converter

Converts CSV columns containing GPS data as produced by ODK Collect
into WKT format (readable by QGIS).

## How to install

1. `git clone http://github.com/zestyping/odk_csv`

2. Move or copy the `odk_csv` directory created by step 1 into your QGIS application's `python/plugins` folder.  This folder is at `$HOME/.qgis2/python/plugins` on Mac/Linux and at `C:\Users\<user>\python\plugins` on Windows.

3. Restart QGIS.

4. In Plugins > Manage Plugins..., type "odk" in the search box, find the "ODK CSV converter" plugin, and click its check box to turn it on.

## Open source license

Copyright 2017 Ka-Ping Yee

Licensed under the Apache License, Version 2.0 (the "License"); you may not
use this file except in compliance with the License.  You may obtain a copy
of the License at: http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.

