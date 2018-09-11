import pywemo

# Total number of wemo devices inside the broadcast domain
NUM_WEMO_DEVICES = 12

# Context: dumb_switch is just a button that looks like a light switch.
#          It is always powered on but does not actually sit in the flow of the circuit.
#          We use this "button" switch to be the 2nd location of the three way switch.
#          If either side is pressed (toggled) the other side should match.  
#          This allows for the dumb button switch to control the other side of the pair.
#          real_switch is the actual switch that should be controlled (the other side of the pair)
#
# Prereqs: You need to know the MAC addresses of both sides of the three-way switch.
#          See discove_all.py for help with doing this part.
#          This seemed to be the simplist way to setup the switch without doing anything crazy
#          like editing the name of the switch and searching for some spcific name (I thought about doing this)

class ThreeWaySwitch:
  def __init__(self, regsub, name, dumb_switch_mac, real_switch_mac):
    self.name = name
    self.real_switch = None # set during discovery 
    self.real_switch_mac = real_switch_mac
    self.dumb_switch = None # set during discovery
    self.dumb_switch_mac = dumb_switch_mac
    self.regsub = regsub # pywemo RegistrySubscription() type

  def discover(self):
    while self.real_switch == None or self.dumb_switch == None: 
      print("Searching for \"%s\" devices ... " % self.name, end='')
      devices = pywemo.discover_devices()
      print("saw %d/%d devices." % (len(devices) , NUM_WEMO_DEVICES))
      for d in devices:
        if d.mac == self.real_switch_mac: 
          self.real_switch = d
        if d.mac == self.dumb_switch_mac: 
          self.dumb_switch = d
    print ("real_switch:     {:24}{:24}{:12}".format(
             self.real_switch.name, 
             self.real_switch.host, 
             self.real_switch.mac)
          )
    print ("dumb_switch:  {:24}{:24}{:12}".format(
             self.dumb_switch.name, 
             self.dumb_switch.host, 
             self.dumb_switch.mac)
          )

  def sync(self):
    self.real_switch.set_state(0)
    self.dumb_switch.set_state(0)

  def register_callbacks(self):
    self.regsub.register(self.real_switch)
    self.regsub.register(self.dumb_switch)
    self.regsub.on(self.real_switch, "BinaryState", self.toggle_callback)
    self.regsub.on(self.dumb_switch, "BinaryState", self.toggle_callback)
    print()

  def toggle_callback(self, device, cb_type, value):
    print ("  {:16}{:24}{:24}{:12}".format(self.name, device.name, cb_type, value))
    if device.mac == self.real_switch.mac:
      self.dumb_switch.set_state(value)
    if device.mac == self.dumb_switch.mac:
      self.real_switch.set_state(value)


if __name__ == "__main__":
  regsub = pywemo.SubscriptionRegistry()
  
  # three way switches: (Name, dummy switch MAC, real_switch switch MAC)
  kitchen = ThreeWaySwitch(regsub, "Kitchen Dimmer", "24F5A25D64CC", "58EF68BB617A") 
  foyer = ThreeWaySwitch(regsub, "Foyer Dimmer", "94103E4E72A0", "58EF68BB756C")
  all_3ways = [kitchen, foyer]
  
  print ("--- Starting discovery of %d three-way circuits ---" % len(all_3ways))
  for tw in all_3ways:
    tw.discover()
    tw.sync()
    tw.register_callbacks()
  
  print ("--- Starting callback handler loop ---")
  regsub.start()
