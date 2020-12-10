import subprocess
from .vpn import VPN


def run_cmd(cmd: str):
    proc = subprocess.run(
        ['bash', '-c', cmd], capture_output=True)
    if proc.returncode != 0:
        msg = 'expected exit code 0 from `{}`, got exit code {}: {}'.format(
            cmd, proc.returncode, proc.stdout.decode('unicode_escape'))
        if proc.stderr:
            msg += ' ' + proc.stderr.decode('unicode_escape')
        raise ValueError(msg)


class NordVPN(VPN):
    def connect(self):
        run_cmd('nordvpn connect')

    def disconnect(self):
        run_cmd('nordvpn disconnect')
