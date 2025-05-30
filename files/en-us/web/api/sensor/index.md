---
title: Sensor
slug: Web/API/Sensor
page-type: web-api-interface
browser-compat: api.Sensor
---

{{securecontext_header}}{{APIRef("Sensor API")}}

The **`Sensor`** interface of the [Sensor APIs](/en-US/docs/Web/API/Sensor_APIs) is the base class for all the other sensor interfaces. This interface cannot be used directly. Instead it provides properties, event handlers, and methods accessed by interfaces that inherit from it.

This feature may be blocked by a [Permissions Policy](/en-US/docs/Web/HTTP/Guides/Permissions_Policy) set on your server.

{{InheritanceDiagram}}

When initially created, the `Sensor` object is _idle_, meaning it does not take measures. Once the {{domxref("Sensor.start()", "start()")}} method is called, it prepares itself to read data and, once ready, the {{domxref("Sensor/activate_event", "activate")}} event is sent and the sensor becomes _activated_. It then sends a {{domxref("Sensor/reading_event", "reading")}} event each time new data is available.

In case of an error, the {{domxref("Sensor/error_event", "error")}} event is sent, reading stops, and the `Sensor` object becomes _idle_ again. The {{domxref("Sensor.start()", "start()")}} method needs to be called again before it can read further data.

## Interfaces based on `Sensor`

Below is a list of interfaces based on the `Sensor` interface.

- {{domxref('Accelerometer')}}
- {{domxref('AmbientLightSensor')}}
- {{domxref('GravitySensor')}}
- {{domxref('Gyroscope')}}
- {{domxref('LinearAccelerationSensor')}}
- {{domxref('Magnetometer')}}
- {{domxref('OrientationSensor')}}

## Instance properties

- {{domxref('Sensor.activated')}} {{ReadOnlyInline}}
  - : Returns a boolean value indicating whether the sensor is active.
- {{domxref('Sensor.hasReading')}} {{ReadOnlyInline}}
  - : Returns a boolean value indicating whether the sensor has a reading.
- {{domxref('Sensor.timestamp')}} {{ReadOnlyInline}}
  - : Returns the timestamp of the latest sensor reading.

## Instance methods

- {{domxref('Sensor.start()')}}
  - : Activates one of the sensors based on `Sensor`.
- {{domxref('Sensor.stop()')}}
  - : Deactivates one of the sensors based on `Sensor`.

## Events

- {{domxref('Sensor.activate_event', 'activate')}}
  - : Fired when a sensor becomes activated.
- {{domxref('Sensor.error_event', 'error')}}
  - : Fired when an exception occurs on a sensor.
- {{domxref('Sensor.reading_event', 'reading')}}
  - : Fired when a new reading is available on a sensor.

## Specifications

{{Specifications}}

## Browser compatibility

{{Compat}}
