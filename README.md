# SmartParking
This is a project that was realized as part of a bachelor project in december 2017.
The basic though is the implementation of a Smart Parking concept with the help of a Raspberry Pi (2nd Gen), an ultra sonic sensor and Amazon Web Services.

## Architecture
![Image Architecture](https://github.com/dernicolas/SmartParking/blob/master/images/architecture.PNG)

The architecture consists of a ultra sonic sensor that sends data to a Rasperry Pi. On the Rasperry Pi a Python script processes the data recieved by the sensor and automatically transfers messages via MQTT to an AWS IoT instance. There the realtime Data can be stored in an AWS Dynamo Database. The data can then be analysed and transformed.

## Prototype
![Image Prototype](https://github.com/dernicolas/SmartParking/blob/master/images/prototype.PNG)

The Prototype was modeled with the help of a acrylic glass surface that inherited 2 ultra sonic sensor underneath that were connected to the Raspberry Pi. More over for each ultra sonic sensor a red lamp was added that would shine red when a parking slot was occupied and green when it was freee. The cabeling looked roughly like this:

![Image Cabeling](https://github.com/dernicolas/SmartParking/blob/master/images/cabeling.png)
