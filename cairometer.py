##    cairo demos Copyright  (C)  2007 Donn.C.Ingle
##
##    Contact: donn.ingle@gmail.com - I hope this email lasts.
##
##    This program is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation; either version 2 of the License, or
##     ( at your option )  any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program; if not, write to the Free Software
##    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

# https://www.cairographics.org/cookbook/animationrotation/

import pygtk
import gtk, gobject, cairo
import math
import time
import random

from gtk import gdk

class Screen( gtk.DrawingArea ):
    """ This class is a Drawing Area"""
    def __init__(self):
        super(Screen,self).__init__()
        ## Old fashioned way to connect expose. I don't savvy the gobject stuff.
        self.connect ( "expose_event", self.do_expose_event )
        ## This is what gives the animation life!
        gobject.timeout_add( 33, self.tick ) # Go call tick every 50 whatsits.

    def tick ( self ):
        ## This invalidates the screen, causing the expose event to fire.
        self.alloc = self.get_allocation ( )
        rect = gtk.gdk.Rectangle ( self.alloc.x, self.alloc.y, self.alloc.width, self.alloc.height )
        self.window.invalidate_rect ( rect, True )
        return True # Causes timeout to tick again.

    ## When expose event fires, this is run
    def do_expose_event( self, widget, event ):
        self.cr = self.window.cairo_create( )
        ## Call our draw function to do stuff.
        pocketchipscreen = [480,270]
        #self.draw( *self.window.get_size( ) )
        self.draw( *pocketchipscreen)

class Gauge ( Screen ):
    """This class is also a Drawing Area, coming from Screen."""
    def __init__ ( self ):
        Screen.__init__( self )

        self.meter = 0

    def draw( self, width, height ):
        ## A shortcut
        cr = self.cr

        self.meter += 0.1
        if self.meter > 3: self.meter=0
        graph = Meter(-60,60)
        graph.dial(cr,self.meter)
        vgraph = Meter(60,0)
        vgraph.dial(cr,self.meter)



class Meter:
    def __init__(self,tx,ty):
        self.ctx = ''
        ## screen width of PocketC.H.I.P.
        self.w = 400
        self.h = 280
        ## tx,ty is offset translation
        self.tx = tx
        self.ty = ty
        ## sx,sy is to change scale
        self.sx, self.sy = 0.25, 0.25
        ## center
        self.xc = 0
        self.yc = 0
        ## edges of gauge
        self.langle = 135.0 * (math.pi/180.0)
        self.rangle = 45.0 * (math.pi/180.0)
        ## for needle on dial
        self.meter = 0

    def dial(self, ctx, val):
        radius = self.h
        # angles are spec'd in radians:
        angle1 = self.langle
        angle2 = self.rangle
        # some color presets:
        bez_color = [0., 0., 0., 1]
        needle_color = [1, 0.2, 0.2, 1]
        inner_color = [1,1,1,0.8]

        #apply transform
        div = 2
        matrix = cairo.Matrix ( 1, 0, 0, 1, self.w/div, self.h/div )
        #matrix = cairo.Matrix ()
        ctx.save()
        cairo.Matrix.translate( matrix, self.tx, self.ty ) # move it
        cairo.Matrix.scale( matrix, self.sx, self.sy ) # Now scale it all
        ctx.transform ( matrix ) # Make it so...
        # 'bezel' or arc frame
        ctx.set_source_rgba(*bez_color)
        ctx.set_line_width(10.0)
        ctx.arc(self.xc, self.yc, radius, angle1, angle2)
        ctx.line_to(self.xc,self.yc)
        ctx.close_path()
        ctx.stroke_preserve()
        ctx.set_source_rgba(*inner_color)
        ctx.fill()

        # center point
        ctx.set_source_rgba(*needle_color)
        ctx.set_line_width(6.0)
        ctx.arc(self.xc, self.yc, 10.0, 0, 2*math.pi)
        ctx.fill()
        needle = ((val * (angle1 - angle2)) + angle1)
        ctx.arc(self.xc, self.yc, radius, needle, needle)
        ctx.line_to(self.xc, self.yc)
        ctx.stroke()
        ctx.restore()


def run():
    window = gtk.Window( )
    window.connect( "delete-event", gtk.main_quit )
    window.set_size_request ( 400, 272 )
    widget = Gauge()
    widget.show( )
    window.add( widget )
    window.present( )
    gtk.main( )
print ("version 2")
run()
