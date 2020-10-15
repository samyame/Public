# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 19:59:45 2020

@author: Sam
"""

import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()