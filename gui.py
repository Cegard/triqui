import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from triqui import *


class Cell(Gtk.ToggleButton):
	
	
	def __init__(self, position):
		Gtk.Label.__init__(self)
		self.position = position


class Dialog(Gtk.Dialog):

    def __init__(self, parent, message):
        Gtk.Dialog.__init__(self, "Fin del juego", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(150, 100)
        label = Gtk.Label(message)
        box = self.get_content_area()
        box.add(label)
        self.show_all()



class Game(Gtk.Window):
	
	
	def __init__(self):
		Gtk.Window.__init__(self, title = "Triqui")
		self.board = [' '] * 10
		self.player_char = ""
		self.agent_char = ""
		self.win_message, self.lose_message, self.draw_message = \
				"Ganaste! Volver a jugar?", \
				"Perdiste! Volver a jugar?", \
				"Empate! Volver a jugar?"
		self.main_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL) 
		self.header_box = Gtk.Box()
		self.add(self.main_box)
		self.main_box.pack_start(self.header_box, True, True, 0)
		self.button_x = Gtk.ToggleButton(label = "X")
		self.button_x.connect("clicked", self.__on_button_x_clicked)
		self.header_box.pack_start(self.button_x, True, True, 0)
		self.button_o = Gtk.ToggleButton(label = "O")
		self.button_o.connect("clicked", self.__on_button_o_clicked)
		self.header_box.pack_start(self.button_o, True, True, 0)
	
	
	def __disable_all(self):
		
		for position in self.cells:
			self.cells[position].set_sensitive(False)
	
	
	def __clean(self):
		self.main_box.remove(self.table)
		self.board = [' '] * 10
	
	
	def __show_message(self, message):
		dialog = Dialog(self, message)
		response = dialog.run()
		
		if response == Gtk.ResponseType.OK:
			self.__clean()
			
			if self.player_char == "X":
				self.button_x.set_active(False)
			
			else:
				self.button_o.set_active(False)
			
			self.__clean()
			self.button_o.set_sensitive(True)
			self.button_x.set_sensitive(True)
		
		else:
			self.close()
		
		dialog.destroy()
	
	
	def __end_game(self, message):
		self.__disable_all()
		self.__show_message(message)
	
	
	def __make_move(self):
		position = getComputerMove(self.board, self.agent_char)
		self.cells[position].set_label(self.agent_char)
		self.cells[position].set_sensitive(False)
		self.board[position] = self.agent_char
		
		if isWinner(self.board, self.agent_char):
			self.__end_game(self.lose_message)
		
		elif isBoardFull(self.board):
			self.__end_game(self.draw_message)
	
	
	def __on_cell_clicked(self, widget):
		widget.set_label(self.player_char)
		widget.set_sensitive(False)
		self.board[widget.position] = self.player_char
		
		if isWinner(self.board, self.player_char):
			self.__end_game(self.win_message)
		
		elif not isBoardFull(self.board):
			self.__make_move()
		
		else:
			self.__end_game(self.draw_message)
	
	
	def __deactivate_buttons(self):
		self.button_x.set_sensitive(False)
		self.button_o.set_sensitive(False)
	
	
	def __assign_chars(self, player, agent):
		self.player_char = player
		self.agent_char = agent
	
	
	def __transform_index(self, position, factor, length):
		first_term = length*factor - 1
		new_position = first_term - position + 1
		
		return new_position
	
	
	def __add_table(self):
		self.table = Gtk.Grid(column_homogeneous = True, column_spacing = 0,
							  row_spacing = 50)
		self.main_box.pack_start(self.table, True, True, 0)
		self.table.show()
		self.cells = {}
		length = 3
		width, height = 1, 2
		max_index = length**2 - 1
		factor = 7
		
		for row in range(length):
			factor -= 2
			
			for col in range(length):
				raw_position = max_index - (length*row + col)
				position = self.__transform_index(raw_position, factor, length)
				cell = Cell(position)
				cell.connect("toggled", self.__on_cell_clicked)
				cell.show()
				self.cells[position] = cell
				self.table.attach(cell, col, row, width, height)
	
	
	def __prepare_game(self, human, agent):
		self.__assign_chars(human, agent)
		self.__deactivate_buttons()
		self.__add_table()
		
		if random.randint(0, 1) == 0:
			self.__make_move()
	
	
	def __on_button_x_clicked(self, widget):
		chars = "XO"
		self.__prepare_game(*chars)
	
	
	def __on_button_o_clicked(self, widget):
		chars = "OX"
		self.__prepare_game(*chars)


win = Game()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()