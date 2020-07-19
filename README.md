# AnimatedLEDStrip Client Library for Python

[![Build Status](https://travis-ci.com/AnimatedLEDStrip/client-python.svg?branch=master)](https://travis-ci.com/AnimatedLEDStrip/client-python)
[![PyPI](https://img.shields.io/pypi/v/animatedledstrip-client.svg)](https://pypi.python.org/pypi/animatedledstrip-client)

This library allows a Python 3 client to connect to an AnimatedLEDStrip server, allowing the client to send animations to the server and receive currently running animations from the server, among other information.

## Creating an `AnimationSender`
An `AnimationSender` is constructed with two arguments:
- `ip_address`: The IP address of the server (as a string)
- `port_num`: The port that the client should connect to (as an integer)

```python
sender = AnimationSender("10.0.0.254", 5)
```

## Starting an `AnimationSender`
An `AnimationSender` is started by calling the `start()` method on the instance.

```python
sender.start()
```

## Stopping the `AnimationSender`
An `AnimationSender` is started by calling the `end()` method on the instance.

```python
sender.end()
```

## Sending Data
An animation can be sent to the server by creating an instance of the `AnimationData` class, then calling `send_animation()` with the instance as the argument.

```python
color = ColorContainer()
color.add_color(0xFF)
color.add_color(0xFF00)

data = AnimationData()
data.add_color(color)

sender.send_animation(data)
```

#### `AnimationData` type notes
The Python library uses the following values for `continuous` and `direction`:
- `continuous`: `None`, `True`, `False`
- `direction`: `Direction.FORWARD`, `Direction.BACKWARD`

## Receiving Data
Received animations are saved to the `running_animations` dict and removed when an `EndAnimation` is received for that animation.

In addition, the Python library uses callbacks that run functions to allow you to specify what to do with data that is received.

### ReceiveCallback
The `receiveCallback` is called whenever the sender receives `bytes` from the server.
The `bytes` are passed to your callback.
Use the `newAnimationDataCallback`, `newAnimationInfoCallback`, `newEndAnimationCallback`, `newSectionCallback` *(Coming soon)* and `newStripInfoCallback` *(Coming soon)* callbacks to handle each type of data.
Runs before `newAnimationDataCallback`, `newAnimationInfoCallback`, `newEndAnimationCallback`, `newSectionCallback` and `newStripInfoCallback`.

```python
def receiveData(data: bytes):
    # Your code here

sender.receiveCallback = receiveData
```

### NewAnimationDataCallback
The `newAnimationDataCallback` is called whenever the sender receives an `AnimationData` instance from the server.
The `AnimationData` instance is passed to your callback.
Runs after the `receiveCallback`.

```python
def processAnimationData(data: 'AnimationData'):
    # Your code here

sender.newAnimationDataCallback = processAnimationData
```

### NewAnimationInfoCallback
The `newAnimationInfoCallback` is called whenever the sender receives an `AnimationInfo` instance from the server.
The `AnimationInfo` instance is passed to your callback.
Runs after the `receiveCallback`.

```python
def handleNewAnimationInfo(info: 'AnimationInfo'):
    # Your code here

sender.newAnimationInfoCallback = handleNewAnimationInfo
```

### NewEndAnimationCallback
The `newEndAnimationCallback` is called whenever the sender receives an `EndAnimation` instance from the server.
The `EndAnimation` instance is passed to your callback.
Runs after the `receiveCallback`.

```python
def handleEndAnimation(anim: 'EndAnimation'):
    # Your code here

sender.newEndAnimationCallback = handleEndAnimation
```

### NewSectionCallback *(Coming soon)*
The `newSectionCallback` is called whenever the sender receives a `Section` instance from the server.
The `Section` instance is passed to your callback.
Runs after the `receiveCallback`.

```python
def newSectionHandler(sect: 'Section'):
    # Your code here

sender.newSectionCallback = newSectionHandler
```

### NewStripInfoCallback *(Coming soon)*
The `newStripInfoCallback` is called whenever the sender receives a `StripInfo` instance from the server.
The `StripInfo` instance is passed to your callback.
Runs after the `receiveCallback`.

```python
def processStripInfo(info: 'StripInfo'):
    # Your code here

sender.newStripInfoCallback = processStripInfo
```
