# vpinball_config_tests
To test the new configgen:
Copy:
1) vpinballGenerator.py to /usr/lib/python3.11/site-packages/configgen/generators/vpinball/vpinballGenerator.py
2) es_features.cfg to /usr/share/emulationstation/es_features.cfg
3) ssh to your batocera machine, then restart emulationstation:
batocera-es-swissknife --restart
4) if you want to keep the modifications (until the next upgade):
batocera-save-overlay

Now, when launching a table, the VPinballX.ini is copied to VPinballX-configgen.ini, which is then modified. So your precious VPinballX.ini should never be overwritten by this damn configgen;-)
Also note, that the <table>.ini file will always override the settings from the configgen.

Tested tables: 
1) avatar for the pinmame window
2) Bad cats with the fulldmd b2s from https://vpuniverse.com/files/file/9591-bad-cats-williams-1989-b2s-with-full-dmd/ for b2s 
3) Cyberrace with fulldmd from https://vpuniverse.com/files/file/17823-cyberrace-original-2023-b2s/
for flexdmd (and b2s)

