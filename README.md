#  Digital Network Model 2.4 GHz (Mesh Topology)

 **Language:** [🇬🇧 English](#) | [🇵🇱 Polish](README_PL.md)

---

![Status](https://img.shields.io/badge/status-concept-blue)
![Technology](https://img.shields.io/badge/network-mesh-green)
![Frequency](https://img.shields.io/badge/2.4GHz-ISM-orange)
![License](https://img.shields.io/badge/license-educational-lightgrey)

---

##  Overview

This project presents a conceptual model of a **short-range digital mesh communication network**, designed for operation in challenging environments such as:

* buildings
* tunnels
* underground infrastructure

---

## 📡 Network Topology (Mesh)

```mermaid
graph LR
    Node1["Node 1 (Base)"] 
    Node2["Node 2 (Relay)"]
    Node3["Node 3 (Relay)"]
    Node4["Node 4 (Group)"]

    Node1 <--> Node2
    Node2 <--> Node3
    Node3 <--> Node4
```

---

## ⚙️ Technical Specification

* **Frequency:** 2405–2480 MHz (ISM band)
* **Modulation:** DSSS
* **Encryption:** AES-128
* **Voice Coding:** CVSD
* **Mode:** Full-Duplex

---

##  VHF vs 2.4 GHz Comparison

| Feature  | VHF       | 2.4 GHz Mesh |
| -------- | --------- | ------------ |
| Range    | very long | medium       |
| Indoor   | poor      | excellent    |
| Security | low       | high         |

---

##  Signal Attenuation

| Material | Impact   |
| -------- | -------- |
| Glass    | minimal  |
| Wood     | medium   |
| Brick    | high     |
| Concrete | critical |
| Metal    | blocking |

---

##  Use Cases

* indoor communication
* emergency systems
* industrial networks
* tactical operations

---

##  Disclaimer

Educational use only.
Unauthorized radio usage may be illegal.

---

##  Author

Concept project – Mesh Network 2.4 GHz
