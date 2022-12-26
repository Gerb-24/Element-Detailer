import sys
import os
import traceback
from PyQt6.QtWidgets import ( 
    QApplication,
    QWidget,
    QLineEdit, 
    QPushButton, 
    QFileDialog, 
    QHBoxLayout, 
    QVBoxLayout, 
    QScrollArea, 
    QLayout, # for setting a layout to have a fixed size
    QGroupBox, 
    QFrame, # for setting the QScrollArea to have no frame
    )
from PyQt6 import uic, QtCore
from PyQt6.QtGui import QIcon, QFont
from detailing import detailMultipleElements 
import json



class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui2.ui', self)
        self.setWindowTitle("Element Detailer")
        self.setWindowIcon(QIcon('ui_images/appicon.ico'))
        self.setFixedSize(self.size())
        self.font = QFont( 'Lato Light', 8 )

        # general data
        self.data = {
            # global settings for ed
            'ed_file':              '',
            'ed_dir':               '',
            'ed_save':              'False',
            # data for ed queue
            'ed_type':              '',
            'ed_proto_file':        '',
            'ed_proto_base':        '',
            'ed_proto_dir':         '',
            'ed_texvar':            '',

            #global settings for tv
            'tv_file':              '',
            'tv_dir':               '',
            'tv_save':              'False',
            # data for tv queue
            'tv_texture':           '',
            'tv_variable':          '',

            # settings for third section
            'root_dir':             '',
            'vmf_file':             '',
            'vmf_dir':              '',
            'ed_type_2':            '',
            'proto_dir':            '',
            'proto_name':           '',
        }

        # string data
        self.le_data = {
            'ed_texvar':    self.ed_texvar_le,
            'tv_texture':   self.tv_texture_le,
            'tv_variable':  self.tv_variable_le,
            'proto_name':   self.proto_name_le,
        }

        # file data
        self.file_le_data = {
            'ed_file':          self.ed_file_le,
            'ed_proto_file':    self.ed_proto_file_le,
            'tv_file':          self.tv_file_le,
            'vmf_file':         self.vmf_file_le,
        }

        self.file_btn_data = {
            'ed_file':          self.ed_file_btn,
            'ed_proto_file':    self.ed_proto_file_btn,
            'tv_file':          self.tv_file_btn,
            'vmf_file':         self.vmf_file_btn,
        }

        self.file_dir_data = {
            'ed_file':          'ed_dir',
            'ed_proto_file':    'ed_proto_dir',
            'tv_file':          'tv_dir',
            'vmf_file':         'vmf_dir',
        }

        self.file_type_data = {
            'ed_file':          'ed',
            'ed_proto_file':    'vmf',
            'tv_file':          'tv',
            'vmf_file':         'vmf',
        }

        self.file_rel_root = {
            'ed_proto_file':    'root_dir'
        }

        # dir data
        self.dir_le_data = {
            'proto_dir':        self.proto_dir_le,
            'root_dir':         self.root_dir_le,
        }

        self.dir_btn_data = {
            'proto_dir':        self.proto_dir_btn,
            'root_dir':         self.root_dir_btn,
        }

        # radio button data
        self.rb_btn_data = {
            'ed_type':  {
                'top':       self.ed_top_btn,
                'side':      self.ed_side_btn,
                'bigside':   self.ed_bigside_btn,
                'corner':    self.ed_corner_btn,
                },
            'ed_type_2':  {
                'top':       self.ed_top_btn_2,
                'side':      self.ed_side_btn_2,
                'bigside':   self.ed_bigside_btn_2,
                'corner':    self.ed_corner_btn_2,
                }
        }

        self.rb_bool_data = {
            'ed_type':  {
                'top':       True,
                'side':      False,
                'bigside':   False,
                'corner':    False,
            },
            'ed_type_2':  {
                'top':       True,
                'side':      False,
                'bigside':   False,
                'corner':    False,
                }
        }

        self.rb_default_data = {
            'ed_type':          'top',
            'ed_type_2':        'top',
        }

        # checkbox data
        self.bool_cb_data = {
            'ed_save':      self.ed_save_cb,
            'tv_save':      self.tv_save_cb,
        }

        # list data ( and list initialization )
        self.list_data_init = {
            'ed':       self.ed_v_layout,
            'tv':       self.tv_v_layout,
        }

        self.list_data = {
            'ed':   {
                'btn':          self.ed_add_btn,
                'layout':       self.create_list_layout( 'ed' ),
                'length':       [ 210, 90, 110 ],
                'vars':         [ 'ed_proto_file', 'ed_type', 'ed_texvar' ],
                'is_path':      [ True, False, False ],
                'dir_key':      'ed_dir',
                'file_type':    'ed',
                'save_btn':     self.ed_save_btn,
                'save_as':      'ed_save',
                'file':         'ed_file'

            },
            'tv':   {
                'btn':          self.tv_add_btn,
                'layout':       self.create_list_layout( 'tv' ),
                'length':       [ 120, 280 ],
                'vars':         [ 'tv_variable', 'tv_texture' ],
                'is_path':      [ False, False ],
                'dir_key':      'tv_dir',
                'file_type':    'tv',
                'save_btn':     self.tv_save_btn,
                'save_as':      'tv_save',
                'file':         'tv_file'
            }
        }

        self.list_widget_matrix = {
            'ed':       [
            ],
            'tv':       [
            ],
        }

        self.list_string_matrix = {
            'ed':       [],
            'tv':       [],
        }

        self.file_to_list = {
            'ed_file':      'ed',
            'tv_file':      'tv',
        }

        # save data
        self.save_keys = [
            'vmf_file',
            'vmf_dir',
            'ed_file',
            'ed_dir',
            'tv_file',
            'tv_dir',
            'proto_dir',
            'root_dir',
        ]

        # connecting string logic
        for tex in self.le_data:
            self.le_data[ tex ].textChanged.connect( lambda _, t=tex: self.assign_text_to_var( tex=t ) )       

        # connecting file logic
        for file in self.file_btn_data:
            self.file_btn_data[ file ].clicked.connect( lambda _, f=file: self.load_file( file=f ) ) 

        # connecting dir logic
        for dir_key in self.dir_btn_data:
            self.dir_btn_data[ dir_key ].clicked.connect( lambda _, d=dir_key: self.load_dir( dir_key=d ) )

        # connecting and initialising radiobutton logic
        for var_key in self.rb_btn_data:
            for sub_key in self.rb_btn_data[var_key]:
                self.rb_btn_data[ var_key ][ sub_key ].clicked.connect( lambda _, var=var_key, sub=sub_key: self.set_rb( var_key=var, sub_key=sub ) )
            self.set_rb( var_key=var_key, sub_key=self.rb_default_data[ var_key ] )

        # connecting checkbox logic
        for key in self.bool_cb_data:
            self.bool_cb_data[ key ].clicked.connect( lambda _, k=key: self.assign_bool_to_var( key=k ) )

        # connecting up list logic
        for list_key in self.list_data:
            self.list_data[ list_key ][ 'btn' ].clicked.connect( lambda _, l=list_key :self.add_to_list( list_key=l ) )
            self.list_data[ list_key ][ 'save_btn' ].clicked.connect( lambda _, l=list_key: self.save_list( list_key=l ) )

        # connecting all the other stuff
        self.save_global_btn.clicked.connect( self.save_settings )
        self.compile_btn.clicked.connect( self.compile )
        self.add_new_proto_btn.clicked.connect( self.add_new_proto )

        self.load_settings()

    # string handler
    def assign_text_to_var( self, tex='' ):
        self.data[ tex ] = self.le_data[tex].text()

    # file handler
    def load_file( self, file='' ):
        dir_key = self.file_dir_data[ file ]
        file_type = self.file_type_data[ file ]
        filepath, _ = QFileDialog.getOpenFileName(self, f"Load {file_type}", self.data[ dir_key ], f"{file_type.upper()}(*.{file_type})")
        if filepath == '':
            return
        # when we want a relative path
        if file in self.file_rel_root:
            root_key = self.file_rel_root[ file ]
            root = self.data[ root_key ]
            rel_file_path = os.path.relpath(filepath, start=root)
            self.data[ file ] = rel_file_path
        else:
            self.data[ file ] = filepath
        self.data[ dir_key ] = os.path.dirname(filepath)
        self.file_le_data[ file ].setText( os.path.basename(filepath) )
        if file in self.file_to_list:
            list_key = self.file_to_list[ file ]
            self.file_data_to_list( file=file, list_key=list_key )

    # dir handler
    def load_dir( self, dir_key='' ):
        dirpath = QFileDialog.getExistingDirectory(self, "Open Directory", self.data[ dir_key ])
        if dirpath == '':
            return
        self.data[ dir_key ] = dirpath
        self.dir_le_data[ dir_key ].setText( os.path.basename(dirpath) )

    # multi-bool handler
    def set_rb( self, var_key='', sub_key='' ):
        for key in self.rb_bool_data[ var_key ]:
            self.rb_bool_data[ var_key ][ key ] =  key == sub_key
        self.data[ var_key ] = sub_key

        # stylessheets
        off_style = '''
        QPushButton {
            background-color: #34495e;
            border-radius: 5px;
        }
        QPushButton::hover {
            background-color: #7f8c8d;
            border-radius: 5px;
        }
        '''
        on_style = '''
        QPushButton {
            background-color: #f1c40f;
            border-radius: 5px;
            color: #34495e;
        }
        '''
        
        for key in self.rb_btn_data[ var_key ]:
            stylesheet =  on_style if self.rb_bool_data[ var_key ][ key ] else off_style
            self.rb_btn_data[ var_key ][ key ].setStyleSheet( stylesheet )

    # bool handler
    def assign_bool_to_var( self, key='' ):
        self.data[ key ] = not self.data[ key ]

    # list handlers
    def create_list_layout(self, key ):
        group_box = QGroupBox()
        layout = QVBoxLayout()
        layout.setSpacing( 10 )
        layout.setSizeConstraint( QLayout.SizeConstraint.SetFixedSize)
        group_box.setLayout( layout )

        scroll = QScrollArea()
        scroll.setFrameShape( QFrame.Shape.NoFrame )
        scroll.setWidget( group_box )
        scroll.setWidgetResizable( True )
        scroll.setFixedHeight( 210 )
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.list_data_init[ key ].addWidget( scroll )
        return layout

    def add_to_list( self, list_key='', names_list = []  ):
        # styles for the remove button
        remove_style = '''
QPushButton {
background-color: #c0392b;
}
QPushButton:hover {
background-color: #e74c3c;
}

QPushButton:disabled {
    background-color: #34495e;
    border-radius: 5px;
}
        '''
        
        length_list = self.list_data[ list_key ][ 'length' ]
        is_path_list = self.list_data[ list_key ][ 'is_path' ]
        if not names_list:
            names_list = [ self.data[ key ] for key in self.list_data[ list_key ][ 'vars' ] ]
        widget_list = []

        def add_new_row( length_list, names_list ):
            # create the horizontal layout in which we put row of widgets
            hor_layout = QHBoxLayout()
            hor_layout.setSpacing( 11 )
            for i, length in enumerate( length_list ):
                name = names_list[ i ]
                is_path = is_path_list[ i ]
                if is_path:
                    name = os.path.basename( name )
                line_edit = QLineEdit( name )
                line_edit.setReadOnly( True )
                line_edit.setAlignment( QtCore.Qt.AlignmentFlag.AlignCenter )
                line_edit.setFixedSize( length, 30 )
                line_edit.setFont( self.font )
                line_edit.show()

                hor_layout.addWidget( line_edit )
                widget_list.append( line_edit )

            # create the remove button last
            remove_btn = QPushButton( 'Remove' )
            remove_btn.setStyleSheet( remove_style )
            remove_btn.setFixedSize( 70, 30 )
            remove_btn.setFont( self.font )

            # connecting logic for remove btn
            list_index = self.list_data[ list_key ][ 'layout' ].count()
            remove_btn.clicked.connect( lambda _, l=list_key, i=list_index: self.remove_row( list_key=l, list_index=i ) )
            remove_btn.show()

            hor_layout.addWidget( remove_btn )
            self.list_data[ list_key ][ 'layout' ].addLayout( hor_layout )
        
        self.list_widget_matrix[ list_key ].append( widget_list )
        self.list_string_matrix[ list_key ].append( names_list )
        add_new_row( length_list, names_list )

    def remove_row( self, list_key='', list_index=''):
        # delete items in matrix
        self.list_string_matrix[ list_key ].pop( list_index )
        self.list_widget_matrix[ list_key ].pop( )

        # delete last row from layout
        layout = self.list_data[ list_key ][ 'layout' ]
        row = layout.itemAt( layout.count() - 1 )

        # delete widgets from row
        layout.removeItem( row )
        for i in range( row.count() ):
            widget = row.itemAt( i )
            row.removeItem( widget )
            if not widget:
                continue
            widget = widget.widget()
            widget.deleteLater()

        # update lineedits
        for row_ind, row in enumerate( self.list_widget_matrix[ list_key ] ):
            for le_ind, le in enumerate( row ):
                le.setText( self.list_string_matrix[ list_key ][ row_ind ][ le_ind ] )

    def file_data_to_list( self, file='', list_key='' ):
        file_path = self.data[ file ]
        with open( file_path, 'r' ) as f:
            load_data = json.loads(f.read())
        
        # get rid of everything in the list

        # add in all the new things
        for row in load_data:
            var_keys = self.list_data[ list_key ][ 'vars' ]
            names_list = [ row[ var_key ] for var_key in var_keys ]
            # use the text in the rows, not from the global variables
            self.add_to_list( list_key=list_key, names_list=names_list )
    
    def save_list( self, list_key='' ):
        save_data = []
        var_keys = self.list_data[ list_key ][ 'vars' ]
        for row in self.list_string_matrix[ list_key ]:
            save_row = {}
            for i, string in enumerate( row ):
                save_row[ var_keys[ i ] ] = string
            save_data.append( save_row )

        json_data = json.dumps( save_data, indent=2 )
        save_as_key = self.list_data[ list_key ][ 'save_as' ]
        save_as_bool = self.data[ save_as_key ] # if true then we use 

        dir_key = self.list_data[ list_key ][ 'dir_key' ]
        file_type = self.list_data[ list_key ][ 'file_type' ]
        if not save_as_bool:
            file_key = self.list_data[ list_key ][ 'file' ]
            filepath = self.data[ file_key ]
        else:
            filepath, _ = QFileDialog.getSaveFileName( self, f"Save {file_type}", self.data[ dir_key ], f"{file_type.upper()}(*.{file_type})")
        if filepath == '':
            print( 'nope' )
            return
        with open(filepath, "w") as f:
            f.write( json_data )

    # global handlers
    def save_settings( self ):
        save_data = {}
        for save_key in self.save_keys:
            save_data[ save_key ] = self.data[ save_key ]

        json_data = json.dumps( save_data, indent=2 )
        with open("settings.json", "w") as f:
            f.write(json_data)

    def load_settings(self):
        with open("settings.json", "r") as f:
            load_data = json.loads(f.read())
        for key in load_data:
            self.data[ key ] = load_data[ key ]
        # for tex in self.le_data:
        #     self.le_data[ tex ].setText( self.data[ tex ] )
        for file in self.file_le_data:
            file_path = self.data[ file ]
            if not file_path: continue
            self.file_le_data[ file ].setText( os.path.basename( file_path ) )
            if file in self.file_to_list:
                list_key = self.file_to_list[ file ]
                self.file_data_to_list( file=file, list_key=list_key )
        # for key in self.bool_cb_data:
        #     self.bool_cb_data[ key ].setChecked( self.data[ key ] )
        for dir_key in self.dir_le_data:
            dir_path = self.data[ dir_key ]
            if not dir_path: continue
            self.dir_le_data[ dir_key ].setText( os.path.basename( dir_path ) )

    def compile( self ):
        def texvar_to_texture( texvar, texvar_dic ):
            try:
                texture = texvar_dic[ texvar ]
            except Exception:   
                texture = texvar
            return texture

        def relpath_to_abspath( relpath, root ):
            abs_path = os.path.join( root, relpath )
            return abs_path

        texvar_dic = { row[0]: row[1] for row in self.list_string_matrix[ 'tv' ] }
        detail_keys = [ 'prt', 'mtd', 'tex' ]

        # from texvar to texture
        detail_data = []
        for row in self.list_string_matrix[ 'ed' ]:
            detail_row = {}
            for i, string in enumerate( row ):
                detail_key = detail_keys[ i ]
                if i == 0:
                    string = relpath_to_abspath( string, self.data[ 'root_dir' ] )
                if i == 2:
                    string = texvar_to_texture( string, texvar_dic )
                detail_row[ detail_key ] = string
            detail_data.append( detail_row )


        file_name = self.data[ 'vmf_file' ]
        detailMultipleElements( file_name, detail_data )

    # misculaneous
    def add_new_proto( self ):
        preset_path = f"prototypes/core/{ self.data[ 'ed_type_2' ] }_prototype.vmf"
        with open( preset_path, 'r' ) as f:
            data = f.read()
        dir_path = self.data[ 'proto_dir' ]
        if dir_path == '':
            return 
        file_name = self.data[ 'proto_name' ]
        if file_name == '':
            return
        new_proto_path = os.path.join( dir_path, f'{file_name}.vmf' )
        with open( new_proto_path, 'w' ) as f:
            f.write( data )

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyleSheet(open('./cssfiles/stylesheet.css').read())

    window = MyApp()
    window.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print(' Closing Window ... ')
