import gtk

class FuncMate:
    SENO = 'Seno'
    TRIANGULAR = 'Triangular'
    CUADRADA = 'Cuadrada'

    def __init__(self):
        self.combobox = gtk.combo_box_new_text()
        self.model = self.combobox.get_model()
        self.append(self.CUADRADA)
        self.append(self.SENO)
        self.append(self.TRIANGULAR)
        self.combobox.set_active(0)
        
    def append(self, txt):
        self.combobox.append_text(txt)

    def get_active_text(self):
        active = self.combobox.get_active()
        if active < 0:
            return None
        return self.model[active][0]

    def get_widget(self):
        return self.combobox