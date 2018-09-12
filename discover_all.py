import pywemo

# Total number of wemo devices inside the broadcast domain
NUM_WEMO_DEVICES = 12

def find_and_show_all_wemo_devices():
    devices = {}
    while len(devices) < NUM_WEMO_DEVICES:
        print("discovering devices ... ", end="")
        devices = pywemo.discover_devices()
        print("{}/{}".format(len(devices), NUM_WEMO_DEVICES))

    print("--- {} Devices Found ---".format(len(devices)))
    for d in devices:
        print("  {:24}{:16}{:12}".format(d.name, d.host, d.mac))


if __name__ == "__main__":
    find_and_show_all_wemo_devices()
