'use strict';

module.exports = {

  'browserport'  : 3000,
  'uiport'       : 3001,
  'serverport'   : 8000,

  'styles': {
    'src' : 'ekratia/client/styles/**/*.scss',
    'dest': 'ekratia/static/css'
  },

  'scripts': {
    'src' : 'ekratia/client/js/**/*.js',
    'dest': 'ekratia/static/js'
  },

  'images': {
    'src' : 'ekratia/static/images/**/*',
    'dest': 'ekratia/static/images'
  },

  'fonts': {
    'src' : ['ekratia/client/fonts/**/*'],
    'dest': 'ekratia/static/fonts'
  },

  'views': {
    'watch': [
      'ekratia/templates/**/*.html'
    ],
    'src': 'ekratia/client/views/**/*.html',
    'dest': 'ekratia/client/js/'
  },

  'gzip': {
    'src': 'ekratia/static/**/*.{html,xml,json,css,js,js.map}',
    'dest': 'ekratia/static/',
    'options': {}
  },

  'dist': {
    'root'  : 'ekratia/static'
  },

  'browserify': {
    'entries'   : ['./ekratia/client/js/main.js'],
    'bundleName': 'main.js',
    'sourcemap' : true
  },

  'test': {
    'karma': 'test/karma.conf.js',
    'protractor': 'test/protractor.conf.js'
  }

};
