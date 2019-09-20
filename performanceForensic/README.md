sat utilities package
=====================

Various utilties developed by team SAT@kwai aiming to analyze, collect vital metrics of hardware, operating system, business application, etc.

It is maintained and built by Wu Xi on a regular basis and of course when there is new utility approved by the team.

A short description of the specific utility:

analyzer - utitlies doing data/info analysis
    |-satBlockInfo.py - get storage info when there is RAID controller installed
    |-xsos - Ryan Sawhill Aroha's sosreport examiner
    |-satVerions.py - extract drv/firmware version from sosreport logs
collector - utitlies which collect key information from various sources
    |-satBiosSettings.py - get BIOS settings independent of OEM specific tools
    |-satRms.py - pull various fields from RMS database
poc - proof of concept of they way data/info might be collected/analyzed
    |-wxParser.py - parse BIOS settings from k=v format to JSON
    |-getBios.sh - primeval way of getting bios settings

- Wu Xi, 09-19-2019
