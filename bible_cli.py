#!/usr/bin/env python3

import click
import sqlite3
import sys, os, subprocess
from colorama import init, Fore, Style


init(autoreset=True)

class Bible:
    def __init__(self, book=None) -> None:
        self.db_file = 'bible.db' 
        self.book = book
        self.data = None 
        
        self.table_color = Fore.BLUE
        self.text_color = Fore.YELLOW
             
        try:
            self.con = sqlite3.connect(self.db_file)
            self.cursor = self.con.cursor()
        except:
            os.mkdir(self.db_file)
        finally:
            self.con = sqlite3.connect(self.db_file)
            self.cursor = self.con.cursor()
        
        if self.book:
            self.book = self.book.lower()
            self.data = self.read_db()
            self.display_book()
        else:
            tables = self.get_table_names()
            self.choose_book(tables)
            
    def colored_text(self, text, color) -> str:
        '''
        Returns colored text
        :param: text - string to color
        :param: color - color 
        :return: str
        '''
        return f"{color}{text}{Style.RESET_ALL}"
    
    def choose_book(self, tables: list) -> None:
        '''
        Choose from a list of books in the bible to read
        :param: tables - list of books
        '''
        print("Choose a book to read: ")
        for table in tables:
            print(self.colored_text(f'{table}', self.table_color))

        ans = input()
        if ans:
            self.book = ans
            self.data = self.read_db()
            self.display_book()

    def display_book(self) -> None:
        '''
        Display colored text in terminal
        '''
        p = subprocess.Popen(['less', '-R'], stdin=subprocess.PIPE, stdout=sys.stdout)
        for i,lines in enumerate(self.data, start=1):
            out = self.colored_text(lines, self.text_color) + "\n"
            p.stdin.write(out.encode('utf-8'))
        p.stdin.close()
        p.wait()       
        
    def get_table_names(self) -> list:
            '''
            Function: Retrieve all table names from the database
            :return: list of table names
            '''
            try:
                self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = self.cursor.fetchall()
                return [table[0] for table in tables]
            except sqlite3.Error as e:
                print(f"Exception retrieving table names: {e}")
                return []
            
    def read_db(self) -> list:
        '''
        Read sqlite3 database and return rows
        :return: list of words in the book selected
        '''
        try:
            self.cursor.execute(f'SELECT * FROM {self.book}')
            rows= self.cursor.fetchall()
            return [row[4] for row in rows]
        except Exception as e:
            print(f'Exception reading from the database: {e}')
            return None
        

@click.command()
@click.option("--book", "-b", help="Book of the bible that you wish to view",required=False)
def main(book) -> None:
    if book:
        Bible(book)  
    else:
        Bible()

if __name__ == "__main__":
    main()