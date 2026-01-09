import random
import process_bad_apple

boiler = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<project source="3.8.0" version="1.0">
  This file is intended to be loaded by Logisim-evolution v3.8.0(https://github.com/logisim-evolution/).

  <lib desc="#Wiring" name="0">
    <tool name="Splitter">
      <a name="facing" val="south"/>
      <a name="fanout" val="9"/>
    </tool>
    <tool name="Pin">
      <a name="appearance" val="classic"/>
    </tool>
  </lib>
  <lib desc="#Gates" name="1"/>
  <lib desc="#Plexers" name="2"/>
  <lib desc="#Arithmetic" name="3"/>
  <lib desc="#Memory" name="4"/>
  <lib desc="#I/O" name="5"/>
  <lib desc="#TTL" name="6"/>
  <lib desc="#TCL" name="7"/>
  <lib desc="#Base" name="8"/>
  <lib desc="#BFH-Praktika" name="9"/>
  <lib desc="#Input/Output-Extra" name="10"/>
  <lib desc="#Soc" name="11"/>
  <main name="main"/>
  <options>
    <a name="gateUndefined" val="ignore"/>
    <a name="simlimit" val="1000"/>
    <a name="simrand" val="0"/>
  </options>
  <mappings>
    <tool lib="8" map="Button2" name="Poke Tool"/>
    <tool lib="8" map="Button3" name="Menu Tool"/>
    <tool lib="8" map="Ctrl Button1" name="Menu Tool"/>
  </mappings>
  <toolbar>
    <tool lib="8" name="Poke Tool"/>
    <tool lib="8" name="Edit Tool"/>
    <tool lib="8" name="Wiring Tool"/>
    <tool lib="8" name="Text Tool"/>
    <sep/>
    <tool lib="0" name="Pin"/>
    <tool lib="0" name="Pin">
      <a name="facing" val="west"/>
      <a name="output" val="true"/>
    </tool>
    <sep/>
    <tool lib="1" name="NOT Gate"/>
    <tool lib="1" name="AND Gate"/>
    <tool lib="1" name="OR Gate"/>
    <tool lib="1" name="XOR Gate"/>
    <tool lib="1" name="NAND Gate"/>
    <tool lib="1" name="NOR Gate"/>
    <sep/>
    <tool lib="4" name="D Flip-Flop"/>
    <tool lib="4" name="Register"/>
  </toolbar>
"""

text = boiler

def pin_appearance(in_pin, out_pin):
    global text 
    text += """<a name="appearance" val="custom"/>
    <appear>
      <rect fill="none" height="20" stroke="#000000" width="11" x="50" y="50"/>
      <circ-anchor facing="east" x="60" y="60"/>
      <circ-port dir="in" pin="{in_pin[0]},{in_pin[1]}" x="50" y="60"/>
      <circ-port dir="out" pin="{out_pin[0]},{out_pin[1]}" x="60" y="60"/>
    </appear>"""


def component(name, loc, inputs=1, facing="east", lib=1, width=0, maxv="", appearance=""):
    global text
    loc = (int(loc[0]), int(loc[1]))
    text += f"""<comp """
    if lib != -1: text += f"""lib="{lib}" """ 
    text += f"""loc="({loc[0]},{loc[1]})" name="{name}">
    <a name="inputs" val="{inputs}"/>
    <a name="facing" val="{facing}"/>"""
    if width > 0: text += f"""<a name="width" val="{width}"/>"""
    if maxv != "": text += f"""<a name="max" val="{maxv}"/>"""
    if appearance != "": text += f"""<a name="appearance" val="{appearance}"/>"""
    text += "</comp>"

def wire(start, end):
    global text
    start = (int(start[0]), int(start[1]))
    end = (int(end[0]), int(end[1]))
    text += f"""<wire from="({start[0]},{start[1]})" to="({end[0]},{end[1]})"/>"""

def pin(loc, pins, output=False, facing="east"):
    global text
    loc = (int(loc[0]), int(loc[1]))
    text += f"""<comp lib="0" loc="({loc[0]},{loc[1]})" name="Pin">
    <a name="appearance" val="NewPins"/>
    <a name="width" val="{pins}"/>
    <a name="output" val="{str(output).lower()}"/>
    <a name="facing" val="{facing}"/>
</comp>"""

def splitter(loc, fanout, incoming, facing="south"):
    global text
    loc = (int(loc[0]), int(loc[1]))
    text += f"""<comp lib="0" loc="({loc[0]},{loc[1]})" name="Splitter">
      <a name="facing" val="{facing}"/>
      <a name="incoming" val="{incoming}"/>
      <a name="fanout" val="{fanout}"/>
    </comp>"""

def start_circuit(name):
    global text
    text += f"""<circuit name="{name}">
    <a name="appearance" val="logisim_evolution"/>
    <a name="circuit" val="{name}"/>
    <a name="circuitnamedboxfixedsize" val="true"/>
    <a name="simulationFrequency" val="1.0"/>
    """
def end_circuit():
    global text
    text += f"</circuit>\n"
def end_project():
    global text
    text += f"</project>\n"

full_video = process_bad_apple.downscale_to_array()

def pixel_on(frame, x, y):
    return full_video[frame][y][x]

display_size_x = 12
display_size_y = 9

######### PIXEL SUB-CIRCUITS ###############
bus_start_y = 200
bus_start_x = 150 
bus_gap_width = 10

and_start_y = 300
and_start_x = 500
and_height = 100
and_gap_width = 20
and_width = 50

frames = 439

for pixel_x in range(display_size_x):
    for pixel_y in range(display_size_y):
        start_circuit(f"p{pixel_x}x{pixel_y}")

        # create input bus
        splitter((bus_start_x-10, bus_start_y - 120), 9, 9)
        in_pin_pos = (bus_start_x-10, bus_start_y - 120)
        pin(in_pin_pos, 9)

        # inverted columns 
        for i in range(9):
            start = (bus_start_x + bus_gap_width * i * 2,
                     bus_start_y + 30)
            end =   (start[0],
                     and_start_y + (and_height * frames) + (and_gap_width * frames))
            wire(start, end)

            component("NOT Gate", start, facing="south")

            # connect this wire to non-not gate path
            w2_end = (start[0]+bus_gap_width, start[1] - 30)
            wire((start[0], start[1]-30), w2_end)

            # connect to splitter, w3=up w4=left w5=up
            w3_end = (start[0], bus_start_y - (i+1) * bus_gap_width)
            wire((start[0], start[1]-30), w3_end)

            w4_end = (bus_start_x + i * bus_gap_width, w3_end[1])
            wire(w3_end, w4_end)

            w5_end = (w4_end[0], bus_start_y - 100)
            wire(w4_end, w5_end)

        # non inverted columns
        for i in range(9):
            start = (bus_start_x + bus_gap_width * 2 * i + bus_gap_width,
                     bus_start_y)
            end =   (start[0],
                     and_start_y + (and_height * frames) + (and_gap_width * frames))
            wire(start, end)


        # output or gates
        first_big_or_pos = (and_start_x + frames * bus_gap_width + 100,
                            and_start_y + (63 * 10) / 2 - 25)

        final_or_pos = (and_start_x + frames * bus_gap_width + 250,
                        and_start_y + (7 * 10) / 2 - 25)
                 
        for i in range(7):
            pos = (first_big_or_pos[0], first_big_or_pos[1] + i * 630)
            component("OR Gate", pos, inputs=63)

            # connections to last or gate
            # w1=right w2=up w3=right
            w1_end = (pos[0] + i * bus_gap_width, pos[1])
            wire(pos, w1_end)

            w2_end = (w1_end[0], and_start_y - 20 + i * bus_gap_width)
            wire(w1_end, w2_end)

            w3_end = (final_or_pos[0]-50, w2_end[1])
            wire(w2_end, w3_end)

        component("OR Gate", final_or_pos, inputs=7)
        pin(final_or_pos, 1, True, "west")
       

        # SOP components for each frame
        for frame in range(frames): # 2fps (9 bits -> 512)
            if not pixel_on(frame, pixel_x, pixel_y): continue
       
            and_pos = (and_start_x, and_start_y + (and_height * frame) + (and_gap_width * frame))
            component("AND Gate", and_pos, inputs=9)
           
            # connect wires to input bus
            for i in range(9):
                start = (bus_start_x + bus_gap_width * 2 * (8-i) + bus_gap_width * ((frame >> i) & 1),
                         and_pos[1] + i * 10 - and_height / 2 + 10)
                end =   (and_pos[0] - and_width,
                         and_pos[1] + i * 10 - and_height / 2 + 10)
                wire(start, end)
           
            # connect to or gate
            w1_start = and_pos
            w1_end = (and_pos[0] + 50 + frame * bus_gap_width, and_pos[1])
            wire(w1_start, w1_end)
           
            w2_start = w1_end
            w2_end = (w1_end[0], and_start_y + - 20 + frame * 10)
            wire(w2_start, w2_end)
           
            w3_start = w2_end
            w3_end = (first_big_or_pos[0] - and_width, w2_end[1])
            wire(w3_start, w3_end)

        pin_appearance(in_pin_pos, final_or_pos)
        end_circuit()

########### MAIN DISPLAY ############
pixel_size = (30, 30)
first_pixel_pos = (150, 300)

start_circuit("main")

component("Counter", (50,50), lib=4, width=9, maxv="0x1ff", appearance="classic")
component("Clock", (30,90), lib=0)
wire((30, 70), (30, 90))
pin((40, 140), 1)
wire((40, 140), (40, 70))

for x in range(display_size_x):
    start = (first_pixel_pos[0] + x * pixel_size[0] - 10, first_pixel_pos[1] - int(pixel_size[1]/2))
    end = (start[0], first_pixel_pos[1] + pixel_size[1] * display_size_y)
    wire(start, end)

for y in range(display_size_x):
    start = (first_pixel_pos[0] - 10, first_pixel_pos[1] - int(pixel_size[1]/2) + pixel_size[1] * y)
    end = (start[0] + pixel_size[0] * display_size_x, start[1])
    wire(start, end)

for x in range(display_size_x):
    for y in range(display_size_y):
        pixel_pos = (first_pixel_pos[0] + x*pixel_size[0], first_pixel_pos[1] + y*pixel_size[1])
        component(f"p{x}x{y}", pixel_pos, lib=-1)
        component("LED", pixel_pos, lib=5, facing="west")

end_circuit()

end_project()
print(text)
