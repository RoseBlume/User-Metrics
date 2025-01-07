import os
import platform
import subprocess
import snapcraft
import sys
import plots
def main():
    if platform.system() == 'Linux':
        script_path = os.path.join(os.path.dirname(__file__), '../scripts/update.sh')
        subprocess.run(['bash', script_path])
    plots.runner()
    #snapcraft.runner()
if __name__ == "__main__":
    main()