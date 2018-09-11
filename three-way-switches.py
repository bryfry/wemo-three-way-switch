import pywemo

NUM_WEMO_DEVICES = 12

# Context: dumbswitch is just a button that looks like a light switch

class ThreeWaySwitch:
  def __init__(self, regsub, name, notswitch_mac, dimmer_mac):
    self.name = name
    self.notswitch_mac = notswitch_mac
    self.dimmer_mac = dimmer_mac
    self.dimmer = None # set during discovery 
    self.notswitch = None # set during discovery
    self.regsub = regsub

  def discover(self):
    while self.dimmer == None or self.notswitch == None: 
      print("Searching for \"%s\" devices ... " % self.name, end='')
      devices = pywemo.discover_devices()
      print("saw %d/%d devices." % (len(devices) , NUM_WEMO_DEVICES))
      for d in devices:
        if d.mac == self.dimmer_mac: 
          self.dimmer = d
        if d.mac == self.notswitch_mac: 
          self.notswitch = d
    print ("dimmer:     {:24}{:24}{:12}".format(self.dimmer.name, self.dimmer.host, self.dimmer.mac))
    print ("notswitch:  {:24}{:24}{:12}".format(self.notswitch.name, self.notswitch.host, self.notswitch.mac))

  def sync(self):
    self.dimmer.set_state(0)
    self.notswitch.set_state(0)

  def register_callbacks(self):
    self.regsub.register(self.dimmer)
    self.regsub.register(self.notswitch)
    self.regsub.on(self.dimmer, "BinaryState", self.toggle_callback)
    self.regsub.on(self.notswitch, "BinaryState", self.toggle_callback)
    print()

  def toggle_callback(self, device, cb_type, value):
    print ("  {:16}{:24}{:24}{:12}".format(self.name, device.name, cb_type, value))
    if device.mac == self.dimmer.mac:
      self.notswitch.set_state(value)
    if device.mac == self.notswitch.mac:
      self.dimmer.set_state(value)
        

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


regsub = pywemo.SubscriptionRegistry()

# three way switches: (Name, dummy switch MAC, dimmer switch MAC)
kitchen = ThreeWaySwitch(regsub, "Kitchen Dimmer", "24F5A25D64CC", "58EF68BB617A") 
foyer = ThreeWaySwitch(regsub, "Foyer Dimmer", "94103E4E72A0", "58EF68BB756C")
all_3ways = [kitchen, foyer]

for t in all_3ways:
  t.discover()
  t.sync()
  t.register_callbacks()

print ("--- Starting Callback Handler Loop ---")
regsub.start()
