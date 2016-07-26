import gtk
import math
import cairo

class widgets:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Drawing With Cairo")
        window.connect("destroy", lambda w: gtk.main_quit())
        self.area = gtk.DrawingArea()
        self.area.set_size_request(380, 300)
        window.add(self.area)
        self.area.connect("expose-event", self.firstdraw)
        self.area.show()
        window.show()

    def firstdraw():
        self.context = area.window.cairo_create()
        self.context.rectangle(event.area.x, event.area.y, event.area.width,
            event.area.height)
        self.context.clip()
        self.arcometer()


    def arcometer(self):
        xc = 128.0;
        yc = 128.0;
        radius = 100.0;
        #angles are spec'd in radians:
        angle1 = 45.0  * (math.pi/180.0);
        angle2 = 180.0 * (math.pi/180.0);

        self.context.set_line_width (10.0);
        self.context.arc (xc, yc, radius, angle1, angle2);
        self.context.stroke (cr);

        self.context.set_source_rgba (1, 0.2, 0.2, 0.6);
        self.context.set_line_width (6.0);

        self.context.arc (xc, yc, 10.0, 0, 2*math.pi);
        self.context.fill (cr);

        self.context.arc (xc, yc, radius, angle1, angle1);
        self.context.line_to (xc, yc);
        self.context.arc (xc, yc, radius, angle2, angle2);
        self.context.line_to (xc, yc);
        self.context.stroke ();

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    widgets()
    main()
