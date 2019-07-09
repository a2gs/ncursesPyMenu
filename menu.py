#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Andre Augusto Giannotti Scota (a2gs)
andre.scota@gmail.com

Modulo de menu: Simplest python menu api ever

Classes: 'option' and 'menu'
'''

import curses

class option:
	def __init__(self, t = "", id = 0, xPos = 0, yPos = 0):
		self.title = t
		self.id = id
		self.xPos = xPos
		self.yPos = yPos

	def set_Xpos(self, x):
		self.xPos = x

	def set_ypos(self, y):
		self.yPos = y

	def _set_title(self, t):
		self.title = t
	def _get_title(self):
		return self.title
	Ptitle = property(_set_title, _get_title)

	def _set_id(self, i):
		self.id = i
	def _get_id(self):
		return self.id
	Pid = property(_set_id, _get_id)

class menu:
	def __init__(self,  rot = False,  escExit = False,  intp = False):
		self.menuList = []
		self.rotate = rot
		self.escToEnd = escExit
		self.holdInt = intp

	def sekGetch(self,  stdscr):
		if self.holdInt == True:
			try:
				return stdscr.getch()				
			except(KeyboardInterrupt):
				return 0
		else:
			return stdscr.getch()
		
	def addOpt(self, opt):
		self.menuList.append(opt)
		
	def addOptList(self,  l):
		for i in range(len(l)):
			self.addOpt(l[i])
		
	def __findEscChar(self,  escList,  k):
		i = 0
		tot  = range(len(escList))
		for i in tot:
			if k == escList[i]:
				return i
		return -1
		
	def show(self, stdscr, color_selected_fg, color_selected_bg, color_unselected_fg, color_unselected_bg, initPos = 1,  escapeChars = []):
		k = 0
		currId = initPos
		totOpts = len(self.menuList)
		retId = 0
		retEscPress = 0
		
		curses.curs_set(False)
		
		## TODO: verificar se ha como checar se suporta cores. Se nao, usar bold e reverso: curses.can_change_color
		curses.start_color()
		curses.init_pair(1, color_selected_fg, color_selected_bg) # Normal
		curses.init_pair(2, color_unselected_fg, color_unselected_bg)  # Selecionado

		while True:
			for i in range(totOpts):
				if currId == self.menuList[i].id:
					stdscr.attroff(curses.color_pair(1))
					stdscr.attron(curses.color_pair(2))
				else:
					stdscr.attroff(curses.color_pair(2))
					stdscr.attron(curses.color_pair(1))

				stdscr.addstr(self.menuList[i].xPos, self.menuList[i].yPos, self.menuList[i].title)
				
			stdscr.refresh()

			k = self.sekGetch(stdscr)

			escCi = self.__findEscChar(escapeChars,  k)
			if escCi != -1: #check if any escape key has been pressed
				retId = currId
				retEscPress = escCi
				break
			else: #check the default menu keys control
				if k == 10: #curses.KEY_ENTER
					retId = self.menuList[currId-1].id
					retEscPress = -1
					break
				elif k == curses.KEY_DOWN or k == curses.KEY_RIGHT or k == 9: #TAB
					if currId < totOpts:
						currId += 1
					elif self.rotate == True and currId == totOpts:
						currId = 1
				elif k == curses.KEY_UP or k == curses.KEY_LEFT:
					if currId > 1:
						currId -= 1
					elif self.rotate == True and currId == 1:
						currId = totOpts
				elif k == curses.KEY_HOME:
					currId = 1
				elif k == curses.KEY_END or ((k == 0 or k == 27) and self.escToEnd): # Int_CtrlC or ESC
					currId = totOpts
		
		stdscr.attroff(curses.color_pair(1))
		stdscr.attroff(curses.color_pair(2))
		curses.curs_set(True)		
		return retId, retEscPress
		
def do_menu(stdscr):
	menuListOpts = [	
		option("  Menu 1  ", 1, 1, 1), 
		option("  Menu 2  ", 2, 2, 1), 
		option("  Menu 3  ", 3, 3, 1), 
		option("  Menu 4  ", 4, 4, 1),
		option("   Fim    ", 5, 5, 1)
	]
	escapeChars = [curses.KEY_F1,  curses.KEY_F2,  ord('q')]
	id = 1 #Start selected option
	escPressedIndex = 0
	m = menu(True, True,  True)

	m.addOptList(menuListOpts)
	while True:
		stdscr.clear()
		id, escPressedIndex = m.show(stdscr, curses.COLOR_CYAN, curses.COLOR_BLACK, curses.COLOR_WHITE, curses.COLOR_BLUE, id, escapeChars)
		if id != 5 and escPressedIndex == -1:
			stdscr.addstr(10, 10, "Selectionado: {}. PAUSA".format(id))
			stdscr.getch()
			continue
		elif escPressedIndex != -1: #show return the menu Id or a negative-1 index from escapeChar if any of these keys has been pressed
			stdscr.addstr(10, 10, "Tecla de escape pressionada: {} sobre o id {}".format(escPressedIndex, id))
			stdscr.getch()
		break

def menu_sample(stdscr):
	stdscr.clear()
	stdscr.refresh()
	do_menu(stdscr)
	curses.endwin()
	
def main():
    curses.wrapper(menu_sample)

if __name__ == "__main__":
    main()
