import subprocess
from abc import abstractmethod


def run_cmd(cmd: str):
    proc = subprocess.run(
        ['bash', '-c', cmd], capture_output=True)
    if proc.returncode != 0:
        msg = 'expected exit code 0 from `{}`, got exit code {}: {}'.format(
            cmd, proc.returncode, proc.stdout.decode('unicode_escape'))
        if proc.stderr:
            msg += ' ' + proc.stderr.decode('unicode_escape')
        raise ValueError(msg)


class VPN:
    @abstractmethod
    def connect(self):
        raise NotImplementedError

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError

    def reconnect(self):
        self.disconnect()
        self.connect()


class NordVPN(VPN):
    def connect(self):
        run_cmd('nordvpn connect')

    def disconnect(self):
        run_cmd('nordvpn disconnect')


vpns = {
    'nord': NordVPN,
}


def get_vpn(name: str, *args, **kwargs) -> VPN:
    if name not in vpns:
        raise ValueError(f"Unknown VPN '{name}'")
    return vpns[name](*args, **kwargs)
