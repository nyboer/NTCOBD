#! /usr/bin/env python
# Draws a speedometer type widget, sets up a framework to create multiple widgets on the screen.
# Need to figure out how to animate this, though.
# http://www.tortall.net/mu/wiki/PyGTKCairoTutorial
# https://cairographics.org/samples/

import gtk
import math
import cairo
import random
import time

bg_color = [0.2,0.2,0.2,1]

# Create a GTK+ widget on which we will draw using Cairo
class Screen(gtk.DrawingArea):

    # Draw in response to an expose-event
    __gsignals__ = { "expose-event": "override" }

    # Handle the expose-event by drawing
    def do_expose_event(self, event):

        # Create the cairo context
        cr = self.window.cairo_create()

        # Restrict Cairo to the exposed area; avoid extra work
        cr.rectangle(event.area.x, event.area.y,
                event.area.width, event.area.height)
        cr.clip()

        self.draw(cr, *self.window.get_size())

    def draw(self, cr, width, height):
        # Fill the background with gray
        cr.set_source_rgba(*bg_color)
        cr.rectangle(0, 0, width, height)
        cr.fill()

class Dial(Screen):
    val = 0 #between 0 and 1
    def draw(self,cr,width,height):
        xc = width/2
        yc = height/2
        radius = height/2
        # angles are spec'd in radians:
        angle1 = 135.0  * (math.pi/180.0)
        angle2 = 45.0 * (math.pi/180.0)
        # calc needle position
        needle = ((self.val * (angle1 - angle2)) + angle1)
        # some color presets:
        bez_color = [0., 0., 0., 1]
        needle_color = [1, 0.2, 0.2, 1]
        inner_color = [1,1,1,0.8]

        # 'bezel' or arc frame
        cr.set_source_rgba(*bez_color)
        cr.set_line_width(10.0)
        cr.arc(xc, yc, radius, angle1, angle2)
        cr.line_to(xc,yc)
        cr.close_path()
        cr.stroke_preserve()
        cr.set_source_rgba(*inner_color)
        cr.fill()

        # center point
        cr.set_source_rgba(*needle_color)
        cr.set_line_width(6.0)
        cr.arc(xc, yc, 10.0, 0, 2*math.pi)
        cr.fill()

        # needle
        cr.arc(xc, yc, radius, needle, needle)
        cr.line_to(xc, yc)
        cr.stroke()


# GTK mumbo-jumbo to show the widget in a window and quit when it's closed
def run(Widget):
    window = gtk.Window()
    window.connect("delete-event", gtk.main_quit)
    widget = Widget()
    widget.show()
    window.add(widget)
    window.present()
    gtk.main()

if __name__ == "__main__":
    Dial.val = 1.3
    run(Dial)
