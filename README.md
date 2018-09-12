# Quickstart

```
sudo docker build . -t "wemo-three-way-switch"
sudo docker run --network host -d "wemo-three-way-switch"
```


## Expected image sizes

```
REPOSITORY              TAG                 IMAGE ID            CREATED             SIZE
wemo-three-way-switch   latest              59553fd2c4f4        12 seconds ago      90.6 MB
python                  3.7-alpine          93b16a3d4364        6 days ago          79.4 MB
```

## Successful run output

```
--- Starting discovery of 2 three-way circuits ---
Searching for "Kitchen Dimmer" devices ... saw 11/12 devices.
  real_switch:  Kitchen Dimmer          192.168.34.226          58EF68BB617A
  dumb_switch:  Kitchen - not a switch  192.168.34.229          24F5A25D64CC
"Kitchen Dimmer" devices callback registration complete

Searching for "Foyer Dimmer" devices ... saw 12/12 devices.
  real_switch:  Foyer Dimmer            192.168.34.232          58EF68BB756C
  dumb_switch:  Foyer - not a switch    192.168.34.233          94103E4E72A0
"Foyer Dimmer" devices callback registration complete

--- Starting callback handler loop ---
  Kitchen Dimmer  Kitchen Dimmer          BinaryState             0
  Kitchen Dimmer  Kitchen - not a switch  BinaryState             0
  Foyer Dimmer    Foyer Dimmer            BinaryState             0
  Foyer Dimmer    Foyer - not a switch    BinaryState             0
```
