FROM python3:latest
RUN apt-get update \
    && apt-get install -y \
        wget \
        apt-transport-https \
        libav-tools \
        ffmpeg \
    && wget --directory-prefix /tmp https://repo.nordvpn.com/deb/nordvpn/debian/pool/main/nordvpn-release_1.0.0_all.deb \
    && apt install /tmp/nordvpn-release_1.0.0_all.deb \
    && apt-get update \
    && apt-get install -y nordvpn \
    && rm /tmp/nordvpn-release_1.0.0_all.deb \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean
COPY requirements.txt .
RUN pip install -r requirements.txt
