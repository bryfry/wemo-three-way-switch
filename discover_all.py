# a useful function not really needed for the 3way daemon
#find_and_show_all_wemo_devices()
def find_and_show_all_wemo_devices():
  devices = {}
  while len(devices) < NUM_WEMO_DEVICES:
    print("discovering devices ... ", end='')
    devices = pywemo.discover_devices()
    print("%d/%d" % (len(devices) , NUM_WEMO_DEVICES))

  print ("--- %d Devices Found ---" % len(devices))
  for d in devices:
    print ("  {:24}{:16}{:12}".format(d.name, d.host, d.mac))
