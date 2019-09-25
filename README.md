# Workshop
Workshop examples, Pycom


## Hardware
- Pycomboard ([Documentation](https://docs.pycom.io/gettingstarted/introduction.html))
- Antenna
- Sensors

## Development Tools
- [Atom.io](https://atom.io/) + [pymakr](https://pycom.io/solutions/software/pymakr/) or [Visual Studio Code](https://code.visualstudio.com/) + [pymakr](https://pycom.io/solutions/software/pymakr/)
- [Micropython](https://micropython.org/)
- MQTT

## Services
- [The Things Network](https://www.thethingsnetwork.org/)
- [Grafana](https://grafana.com/)

# Step By Step
## 1 - Assemble the hardware (Pycom board)

## 2 - Install the development tools

## 3 - Connect to the Pycom board

## 4 - Create an application on TTN

### Dev EUI - Get the Mac address
```
from network import LoRa
import ubinascii
lora = LoRa (mode=LoRa.LORAWAN)

ubinascii.hexlify(lora.mac())
```
