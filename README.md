# Wwise Auto Trim
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE.md)


A script used to automatically detect empty space and set trim points on all Audio Source Files in a Wwise project. Commonly referred to as a "strip silence".

**Link to project:** [https://github.com/sawyer-king/WwiseAutoTrim/](https://github.com/sawyer-king/WwiseAutoTrim)

```
This script requires Python, Wwise, WAAPI, PyWwise, and scripy.io to be installed.
```

## Modules:
`auto_trim_all.py`
 - Queries the Wwise project for all Audio File Sources, then checks to see if there is any space with no audio in the wav file, then sets trims points to the sample accurate position where audio begins.

## Additonal Features
Current version adds an InitialDelay offset to keep original sync, can easily remove with comments if you do not want/need that functionality. Looking to add GUI options for this in the next version.

## Examples, Additional Documentation:
Take a look at the PyWwise Wiki, and WAAPI docs for more examples and documentation:

**PyWwise Wiki:** [https://github.com/matheusvilano/PyWwise/wiki](https://github.com/matheusvilano/PyWwise/wiki)

**WAAPI Documentation:** [https://www.audiokinetic.com/en/public-library/2024.1.4_8780/?source=SDK&id=waapi.html](https://www.audiokinetic.com/en/public-library/2024.1.4_8780/?source=SDK&id=waapi.html)
