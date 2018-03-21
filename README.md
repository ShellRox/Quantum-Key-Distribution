# Quantum-Key-Distribution
A modified BB84 protocol utilizing emulated photons for Quantum Key Distribution (QKD).

# Example

Quantum channel is initiated. Both **Bob** (receiver) and **Alice** (sender) known the ip address of this quantum channel.

**input:**

```python
from channel import public_channel
public_channel.initiate_server()
```

**server output:**
```
initiated the channel on xxx.xxx.x.xxx:xxxx, waiting for clients...
```

Bob starts listening to quantum channel.

**input:**

```python
from receiver import receiver
bob = receiver()
bob.connect_to_channel('xxx.xxx.x.xxx', xxxx)
bob.listen_quantum()
```

**server output:**

```
xxx.xxx.x.xxx:xxxx has connected.
```

Alice sends a photon pulse to Bob.

**input:**

```python
from sender import sender
alice = sender()
alice.connect_to_channel('xxx.xxx.x.xxx', xxxx)
photon_pulse = alice.create_photon_pulse()
alice.send_photon_pulse(photon_pulse)
```

**server output:**

```
xxx.xxx.x.xxx:xxxx has connected.
xxx.xxx.x.xxx:xxxx: qpulse:170
xxx.xxx.x.xxx:xxxx: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

Alice and Bob reset their sockets.

**input:**
```python
bob.reset_socket()
```

**input 2:**

```python
alice.reset_socket()
```

After quantum channel is closed, classical channel is initiated. Both Bob and Alice known the ip address of this classical channel.

**input:**

```python
from channel import public_channel
public_channel.initiate_server()
```

Bob listens to public classical channel.

**input:**

```python
bob.connect_to_channel('xxx.xxx.x.xxx', xxxx)
bob.listen_classical()
```

Alice sends her basis to Bob over public classical channel.

**input:**
```python
alice.connect_to_channel('xxx.xxx.x.xxx', xxxx)
alice.send_classical_bits(alice.basis)
```

Alice listens to public classical channel.

**input:**

```python
alice.reset_socket()
alice.connect_to_channel('xxx.xxx.x.xxx', xxxx)
alice.listen_classical()
```

Bob sends his randomly measured basis over public classical channel.
```python
alice.connect_to_channel('xxx.xxx.x.xxx', xxxx)
alice.send_classical_bits(alice.basis)
```

To be continued...
