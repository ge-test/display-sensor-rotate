#!/usr/bin/python

import subprocess, sys

MON='/usr/bin/monitor-sensor'
XR='/usr/bin/xrandr'
SETTINGS='/usr/bin/gsettings'

OR='orientation changed'

OR_MP = {
    'normal': ('normal', 'Left'),
    'bottom-up': ('inverted', 'Left'),
    'right-up': ('right', 'Bottom'),
    'left-up': ('left', 'Bottom'),
}

def get_orientation(line):
    if line.find(OR) == -1:
        return None
    idx = line.rfind(' ')
    if idx == -1:
        idx = line.rfind(':')
    if idx == -1:
        sys.stderr.write('Could not extract orientation from line: "{}"'.format(line))
        return None
    
    idx += 1

    orientation = line[idx:].strip(' \n')
    if orientation not in OR_MP:
        sys.stderr.write('Orientation not understood "{}"'.format(orientation))
        return None

    return OR_MP[orientation]

def service():
    proc = subprocess.Popen([MON],stdout=subprocess.PIPE)

    for line in iter(proc.stdout.readline,''):
        settings = get_orientation(line)
        if not settings:
            continue

        orientation, launcher_position = settings 

        print('Setting orientation to: {}'.format(orientation)) 
        
        subprocess.check_call([XR, '--output', 'eDP-1', '--rotate', orientation])
        subprocess.check_call([SETTINGS, 'set', 'com.canonical.Unity.Launcher', 'launcher-position', launcher_position ])

    

def main():
    while True:
        try:
            service()
        except KeyboardInterrupt:
            return 0
        except Exception as ex:
            sys.stderr.write('Caught exception: {}'.format(ex))


if __name__ == '__main__':
    sys.exit(main())
