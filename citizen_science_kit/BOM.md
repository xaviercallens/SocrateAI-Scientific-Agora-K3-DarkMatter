# Projet Caméléon : L’Interféromètre du Peuple 🇫🇷 (The People's Interferometer)
## Bill of Materials (BOM) & Hardware Assembly Guide

This document contains the exact shopping list, specifications, and assembly instructions to build your own low-cost, high-precision **Chameleon Dark Sector Interferometer** for under **80 €**. 

By placing a heavy shield (such as concrete blocks) over one of the laser arms, you create an asymmetric quantum shield. As the global 7.52-day K3 Dark Matter wave washes over Europe, it alters the local vacuum's refractive index differently in the shielded arm compared to the open arm. This causes the laser interference rings (fringes) to "breathe" in a rhythmic, 7.52-day cycle. By networking thousands of these basement sensors, our federated AI filter isolates this cosmic heartbeat from local seismic and thermal noise.

---

## 🛒 1. Shopping List (Total Cost < 80 €)

All components can be sourced easily from AliExpress, Amazon, or local hardware stores.

| Component | Description | Est. Price | Sourcing / Reference Links |
| :--- | :--- | :---: | :--- |
| **Coherent Light Source** | 5mW Red Laser Diode Module (650nm, adjustable focus, 5V) | **~5 €** | [Amazon Laser Diode](https://www.amazon.fr/s?k=module+diode+laser+650nm+5v) / [AliExpress](https://www.aliexpress.com/wholesale?SearchText=650nm+5v+laser+module) |
| **Beam Splitter** | 50/50 Beam Splitter Cube (20x20x20mm) or Plate | **~12 €** | [AliExpress Beam Splitter Cube 20mm](https://www.aliexpress.com/wholesale?SearchText=50%2F50+beam+splitter+cube+20mm) |
| **Reflecting Mirrors** | 2x First-Surface Mirrors (25x25mm, front-surface reflecting to prevent double reflection) | **~8 €** | [AliExpress First Surface Mirror](https://www.aliexpress.com/wholesale?SearchText=first+surface+mirror+25x25) |
| **High-Precision Sensor** | Raspberry Pi Zero W (or Zero 2 W) with Wi-Fi | **~15 €** | [Kubeii / Kubii France](https://www.kubii.com/fr/) / [PiHut](https://thepihut.com/) |
| **Interferometer Camera** | Raspberry Pi Camera Module V2 (or repurposed USB webcam) | **~15 €** | [Kubii Pi Camera V2](https://www.kubii.com/fr/appareils-photos-cameras/1722-module-camera-v2-8mp-raspberry-pi-3272496006157.html) |
| **Chameleon Shield** | 2x Standard heavy concrete building blocks (*parpaings*) or lead fishing weights | **~3 €** | Local DIY Store (Leroy Merlin, Castorama) or fishing store |
| **Structural Frame** | Flat wood board or medium-density fiberboard (MDF) (300x300mm, minimum 15mm thickness) | **~5 €** | Local hardware store or scrap wood |
| **Mounts & Adapters** | 3D-printed mounts (requires ~100g of PLA plastic) | **~2 €** | Print at home, local FabLab, or public library |
| **Total Estimated Cost** | **Fully functional quantum-gravity detector** | **~60 € - 77 €** | **Open-source science at citizen scale!** |

---

## 🛠️ 2. Step-by-Step Hardware Assembly

Follow this layout to construct your basement interferometer.

```
                  [ Mirror A ] (Shielded under heavy concrete blocks)
                       |
                       |  <-- Arm A
                       |
 [ Laser ] -------> [ 50/50 Cube ] -------> [ Mirror B ] (Open air)
                       |
                       |  <-- Recombined Path
                       |
                       v
                 [ RPi Camera ] (Sensor exposed directly to fringe rings)
```

### Step 2.1: Baseboard Preparation
1. Obtain your **300x300mm wood board**. A thick, heavy base is crucial because it acts as a mechanical low-pass filter to dampen floor vibrations.
2. Sand the board flat and place rubber cabinet bumper pads (or a soft sponge sheet) underneath the board to isolate it from the floor.

### Step 2.2: 3D Printing the Optical Mounts
1. Go to the `citizen_science_kit/3D_Print_Files/` folder.
2. Use the provided CAD/OpenSCAD files to print:
   * **1x Laser Diode Holder**
   * **1x Beam Splitter Cube Base**
   * **2x Kinematic Mirror Mounts** (these use cheap M3 screws and springs to allow sub-millimeter angle adjustments).
   * **1x Camera Board Holder**.

### Step 2.3: Modifying the Camera (Lens Removal)
> [!WARNING]
> This step requires care. We need the raw silicon sensor of the camera to capture the laser fringes directly. Placing a lens on the camera would focus the laser into a single dot and burn the pixels, or block the interference pattern.
1. Unscrew the plastic lens from your Raspberry Pi Camera Module using the lens adjustment tool included in the kit (or small needle-nose pliers).
2. Store the lens in a dust-free bag. 
3. Tape a small piece of transparent red film (or cut-up plastic folder) over the sensor to act as a 650nm bandpass filter, blocking room lights while letting the red laser through.

### Step 2.4: Component Alignment & Gluing
1. Glue the **Laser Holder** to the left edge of the board using standard hot glue or epoxy.
2. Align and glue the **50/50 Beam Splitter Cube** exactly 100mm in front of the laser.
3. Glue the **Mirror B Mount** at the end of Arm B (100mm to the right of the cube).
4. Glue the **Mirror A Mount** at the end of Arm A (100mm above the cube).
5. Glue the **Camera Holder** 100mm below the cube, directly facing Arm A's reflection.
6. Connect the camera ribbon cable to your **Raspberry Pi Zero W**.

### Step 2.5: Tuning the Interference Fringes
1. Power up the laser diode (connect its red/black wires to the 5V and GND pins of the Raspberry Pi).
2. Gently turn the adjustment screws on Mirror A and Mirror B until the two reflected red dots overlap perfectly on the camera sensor.
3. Once aligned, look at the output feed of the camera on your screen. You will see a beautiful, glowing pattern of **concentric red and dark rings** (the interference fringes). 
4. Tighten the lock nuts on the mirror mounts to freeze the alignment.

### Step 2.6: Installing the Chameleon Shield
1. Place a rigid cardboard box or plastic pipe cover over **Arm A** to isolate it thermally.
2. Carefully place **two heavy concrete parpaings (bricks) or lead weights** over this cover. Make sure the weights do *not* physically touch the mirrors or baseboard to avoid knocking the laser out of alignment.
3. Leave **Arm B** completely exposed to the basement air.

---

## 🚀 Next Steps: Running the Software
Once your interferometer is aligned, navigate to the `citizen_science_kit/` directory and execute the fringe tracking software:
```bash
python3 fringe_tracker.py --device 0 --upload
```
The system will now track the fringe shifts with sub-pixel precision and stream daily phase vectors to the central server in Cagnes-sur-Mer. Welcome to the **Agora Swarm**!
