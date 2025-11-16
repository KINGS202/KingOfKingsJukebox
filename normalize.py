import subprocess, os, sys

def normalize(input_path, output_path):
    # Requires ffmpeg installed and in PATH
    cmd = [
        'ffmpeg','-i', input_path, '-af', 'loudnorm=I=-14:LRA=7:TP=-1.5', '-ar', '44100', output_path
    ]
    print('Running:', ' '.join(cmd))
    subprocess.check_call(cmd)

if __name__=='__main__':
    if len(sys.argv)<3:
        print('Usage: python normalize.py input.mp3 output.mp3')
    else:
        normalize(sys.argv[1], sys.argv[2])
