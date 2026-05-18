import os
import sys
import xmltodict
from ncclient import manager

# Hier vertellen we het script welke bestanden en inloggegevens we gebruiken
ROUTER_IP = os.getenv("ROUTER_IP")
ROUTER_USER = os.getenv("ROUTER_USER", "admin")
ROUTER_PASS = os.getenv("ROUTER_PASS")
CONFIG_FILE = "configs/router_virtueel.xml"  # Dit moet exact matchen met jouw XML-bestandsnaam!

def main():
    # Controleer of je wel een IP en wachtwoord hebt opgegeven
    if not ROUTER_IP or not ROUTER_PASS:
        print("[-] Fout: ROUTER_IP en ROUTER_PASS omgevingsvariabelen zijn verplicht!")
        sys.exit(1)

    # 1. Proberen het XML-bestand te openen dat in je configs map staat
    try:
        with open(CONFIG_FILE, "r") as file:
            xml_payload = file.read()
            print(f"[+] Succesvol configuratiebestand ingelezen: {CONFIG_FILE}")
    except FileNotFoundError:
        print(f"[-] Fout: Bestand {CONFIG_FILE} niet gevonden. Controleer de naam!")
        sys.exit(1)

    # 2. Verbinding maken met de Cisco-router
    print(f"[*] Poging tot NETCONF-verbinding met {ROUTER_IP}...")
    try:
        with manager.connect(
            host=ROUTER_IP,
            port=830,
            username=ROUTER_USER,
            password=ROUTER_PASS,
            hostkey_verify=False,
            device_params={'name': 'iosxe'}
        ) as m:
            print(f"[+] Succesvol verbonden met de router via NETCONF!")
            print(f"[*] Aantal ondersteunde router-functies (Capabilities): {len(m.server_capabilities)}")
                    
    except Exception as e:
        print(f"[-] Verbindingsfout: Details: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
