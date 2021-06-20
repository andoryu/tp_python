import math

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from common import random_cities
from nn import calc_paths

class TSWindow(Gtk.Window):

    city_list = []
    path_list = []

    def __init__(self):
        Gtk.Window.__init__(self, title="Travelling Salesman - Python style")

        #win->vertical main container
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.main_box)

        #main->horizontal display container for buttons and canvas
        self.display_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.main_box.pack_start(self.display_box, True, True, 1)

        #main->status bar
        self.status_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.main_box.pack_start(self.status_bar, True, True, 1)

        #display->button bar
        self.button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.display_box.pack_start(self.button_box, True, True, 1)

        #display->canvas
        self.canvas = Gtk.DrawingArea()
        self.canvas.set_size_request(1000, 1000)

        self.canvas.connect("draw", self.do_canvas_draw)
        self.display_box.pack_start(self.canvas, True, True, 1)

        #button bar->edit field - no. of cities
        self.cities = Gtk.Entry()
        self.cities.set_text("35")
        self.button_box.pack_start(self.cities, False, False, 1)

        #button bar->button - randomise cities
        self.randomise = Gtk.Button.new_with_label("Randomise")
        self.randomise.connect("clicked", self.do_random_cities)
        self.button_box.pack_start(self.randomise, False, False, 1)

        #button bar->button - run NN
        self.NN = Gtk.Button.new_with_label("Nearest Neighbour")
        self.NN.connect("clicked", self.do_nn_click)
        self.button_box.pack_start(self.NN, False, False, 1)

        #button bar->button - run GA
        self.GA = Gtk.Button.new_with_label("Genetic Algorithm")
        self.GA.connect("clicked", self.do_ga_click)
        self.button_box.pack_start(self.GA, False, False, 1)

        #status bar->info label
        self.status = Gtk.Label(label=" ")
        self.status_bar.pack_start(self.status, False, False, 2)

    ###
    # event handlers
    def do_random_cities(self, button):
        try:
            num_cities = int(self.cities.get_text())
            self.city_list = random_cities(num_cities, 1000.0)
            self.path_list = []
            self.canvas.queue_draw()
            self.status.set_text(f"{num_cities} cites randomised")
        except Exception as e:
            print(e)
            self.status.set_text("cities needs to be an integer number")


    def do_nn_click(self, button):
        self.path_list = []
        self.canvas.queue_draw()

        path_data = calc_paths(self.city_list)
        self.status.set_text(f"Nearest Neighbour. Distance: {path_data[1]}")

        self.path_list = self.convert_path_data(path_data[0])
        self.canvas.queue_draw()

    def do_ga_click(self, button):
        self.path_list = []
        self.canvas.queue_draw()

        #path_data = calc_paths(self.city_list)
        #self.status.set_text(f"Nearest Neighbour. Distance: {path_data[1]}")

        #self.path_list = self.convert_path_data(path_data[0])
        self.canvas.queue_draw()


    def do_canvas_draw(self, canvas, cr):
        width = canvas.get_allocated_width()
        height = canvas.get_allocated_height()

        #background
        cr.set_source_rgb(0.16, 0.17, 0.20)
        cr.paint()

        #selected paths
        if self.path_list:
            cr.set_source_rgb(1.0, 1.0, 1.0)
            for path in self.path_list:
                cr.move_to(path[0][0], path[0][1])
                cr.line_to(path[1][0], path[1][1])
                cr.stroke()

        #city circles
        if self.city_list:
            ##start city
            cr.set_source_rgb(0.0, 0.65, 0.1)
            self.draw_city(cr, self.city_list[0])

            ##remaining cities
            cr.set_source_rgb(0.0, 0.1, 0.8)
            for city in self.city_list[1:]:
                self.draw_city(cr, city)

        return False

    ###
    #utility handlers
    def draw_city(self, cr, city):
        x = city[1]
        y = city[2]
        radius = 9.0
        angle1 = 0.0
        angle2 = 2.0 * math.pi

        cr.arc(x, y, radius, angle1, angle2)
        cr.fill()

    def convert_path_data(self, data):
        path = []

        pairs = zip(data, data[1:])
        for p in pairs:
            a = p[0]
            b = p[1]

            path.append( [self.city_list[a][1:], self.city_list[b][1:]] )

        return path

win = TSWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()