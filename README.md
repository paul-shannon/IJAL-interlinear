# IJAL-interlinear
render interactive webpage from audio and ELAN markup: a proposal for David Beck

This skeletal python package demonstrates one possible way to refactor EtoHTML.py, with these goals:
  - use traditional Python package module directory structure
  - create some organizing classes: Tier, Annotation, Audio, perhaps Text ...
  - provide a small but full-featured example in testData/: .wav audio file and .eaf markup
  - include automated tests for each class such that ````make test```` in root directory exercises all the code, produces interactive HTML
