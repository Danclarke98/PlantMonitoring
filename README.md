# PlantMonitoring
A houseplant monitoring platform using SQL and MQTT. Created for ESP Microcontrollers.

## Usage

In order to use the platform, users must register an account.


### Device Management -

Once registered users can generates unique ID's to connect indivdual sensors.

![image](https://user-images.githubusercontent.com/43765893/63206323-3a80be80-c0aa-11e9-9d70-65a58eb5a6a6.png)

### Device Details/Sensor Data
When a device is connected to the MQTT server information will be automatically presented using chart.js showing temperature,soil moisture and humdity. 

![image](https://user-images.githubusercontent.com/43765893/63206330-4ff5e880-c0aa-11e9-9764-4505da721528.png)



## Structure

### Use Case

![image](https://user-images.githubusercontent.com/43765893/63206410-bd564900-c0ab-11e9-9ce6-5c1cf81e0353.png)

Users can recieve live information by directly subscribing to the MQTT broker or Historical data via the Web Application.




### Database Schema

![image](https://user-images.githubusercontent.com/43765893/63206338-7d429680-c0aa-11e9-888f-2c51b31a78ac.png)
