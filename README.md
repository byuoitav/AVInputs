# AV Inputs

Script to determine the number of AV inputs on the BYU AV couch database.

## Rules

1. Devices must be of type "D1"
2. Get the room name from the device
3. Get the number of available inputs for the device type
4. Check if the Room has a SW1
5. Check the available inputs for the SW1


### Usage

```console
$ python3 av_inputs.py username password
```