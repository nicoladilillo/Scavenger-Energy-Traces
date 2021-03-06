# Scavenger Energy Traces

Given a set of timestamps and the relative value of environment quantity, for each of that the corresponding power value is produced, assuming perfect MPPT tracking.

## Getting started

In order to use this tool is needed to install a version of python 3.

## Usage

For its usage two main files are needed.

- A file .csv containing all the values of timestamp and the correlate quantity, a possible header could be present.
- One or more file containing a representation of the current/voltage curves, obtaining by digitalization. One single file is used for each curve and its format is *<product_name>_<curve_value>.txt*. Inside it there are a variable number of rows, representing point, each of which is composed by two columns, one for current and one for voltage. In the header are specified the order of magnitude for current and voltage that could be A, mA, uA and pA for the current and V, mV, uV and pV for the voltage (it's also possible to omit the the A and the V).

More curve files means also a more precise result and no matter in which order they are loaded.

To use the tool the following command is needed.
```
python3 script.py timestamp.csv <product_name1>_<curve_value1>.txt ...
```
The result will be a .csv file named *<product_name>_output.csv* where all the values of the last column will become power. The unit of measure of power will be always Watt (W).

## How it works

In first place for each current/voltage curve the MPP is calculated. Then, for all timestamps, the value of power is obtained thorough a linear interpolation of previous calculated MPP value, choosing the proper interval.
If environment quantity is greater that the biggest curve or lower than zero a saturation mechanism is in charge to solve this problem.


