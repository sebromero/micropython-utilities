from network import WLAN, STA_IF
from espnow import ESPNow
import ubinascii

class ESPNowManager:
    def __init__(self):
        self._peers = []

    def add_peer(self, mac_address):
        if mac_address not in self._peers:
            self._peers.append(mac_address)
            try:
                self.esp_now.add_peer(mac_address)
            except Exception:  # Peer already added
                pass

    def remove_peer(self, mac_address):
        if mac_address in self._peers:
            self._peers.remove(mac_address)
            try:
                self.esp_now.del_peer(mac_address)
            except Exception:  # Peer not found
                pass

    @property
    def peers(self):
        return self._peers
    
    def start(self):
        self.wlan = WLAN(STA_IF)
        self.wlan.active(True)
        self.esp_now = ESPNow()
        self.esp_now.active(True)

        mac = self.wlan.config('mac')
        return ubinascii.hexlify(mac, " ").decode()

    def stop(self):
        if self.esp_now:
            self.esp_now.active(False)
            self.esp_now = None
        if self.wlan:
            self.wlan.active(False)
            self.wlan = None

    def get_data(self, timeout=None):
        if not self.esp_now:
            return None, None
        host, data = self.esp_now.recv(timeout)
        if not data:
            return None, None
        host_addr = ubinascii.hexlify(host).decode()
        host_addr_spaces = " ".join(host_addr[i:i+2] for i in range(0, len(host_addr), 2))
        return host_addr_spaces, data

    def get_message(self):
        host, message = self.get_data()
        if message:
            return host, message.decode()

    def send_message(self, peer_mac, message, sync=True):
        if not self.esp_now:
            return False
        mac_trimmed = peer_mac.replace(" ", "")
        # Check for valid MAC address format
        if len(mac_trimmed) != 12 or not all(c in '0123456789abcdefABCDEF' for c in mac_trimmed):
            raise ValueError("Invalid MAC address format")
        peer = bytes.fromhex(mac_trimmed)
        self.add_peer(peer)
        return self.esp_now.send(peer, message, sync)
    
    def send_broadcast(self, message):
        if not self.esp_now:
            return False
        peer = "ffffffffffff"
        return self.send_message(peer, message, False)
