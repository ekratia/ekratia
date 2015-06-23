'use strict';

module.exports = {

  'browserport'  : 3000,
  'uiport'       : 3001,
  'serverport'   : 8000,

  'styles': {
    'src' : 'idekratia/client/styles/**/*.scss',
    'dest': 'idekratia/static/css'
  },

  'scripts': {
    'src' : 'idekratia/client/js/**/*.js',
    'dest': 'idekratia/static/js'
  },

  'images': {
    'src' : 'idekratia/static/images/**/*',
    'dest': 'idekratia/static/images'
  },

  'fonts': {
    'src' : ['idekratia/client/fonts/**/*'],
    'dest': 'idekratia/static/fonts'
  },

  'views': {
    'watch': [
      'idekratia/templates/**/*.html'
    ],
    'src': 'idekratia/client/views/**/*.html',
    'dest': 'idekratia/client/js/'
  },

  'gzip': {
    'src': 'idekratia/static/**/*.{html,xml,json,css,js,js.map}',
    'dest': 'idekratia/static/',
    'options': {}
  },

  'dist': {
    'root'  : 'idekratia/static'
  },

  'browserify': {
    'entries'   : ['./idekratia/client/js/main.js'],
    'bundleName': 'main.js',
    'sourcemap' : true
  },

  'test': {
    'karma': 'test/karma.conf.js',
    'protractor': 'test/protractor.conf.js'
  }

};
