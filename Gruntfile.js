module.exports = function (grunt) {

  var appConfig = grunt.file.readJSON('package.json');

  // Load grunt tasks automatically
  // see: https://github.com/sindresorhus/load-grunt-tasks
  require('load-grunt-tasks')(grunt);

  // Time how long tasks take. Can help when optimizing build times
  // see: https://npmjs.org/package/time-grunt
  require('time-grunt')(grunt);

  var pathsConfig = function (appName) {
    this.app = appName || appConfig.name;

    return {
      app: this.app,
      templates: this.app + '/templates',
      css: this.app + '/static/css',
      sass: this.app + '/static/sass',
      fonts: this.app + '/static/fonts',
      images: this.app + '/static/images',
      js: this.app + '/static/js',
      manageScript: 'manage.py'
    }
  };

  grunt.initConfig({

    paths: pathsConfig(),
    pkg: appConfig,

    // see: https://github.com/gruntjs/grunt-contrib-watch
    watch: {
      gruntfile: {
        files: ['Gruntfile.js']
      },
      compass: {
        files: ['<%= paths.sass %>/**/*.{scss,sass}'],
        tasks: ['compass:server']
      },
      livereload: {
        files: [
          '<%= paths.js %>/**/*.js',
          '<%= paths.sass %>/**/*.{scss,sass}',
          '<%= paths.app %>/**/*.html'
          ],
        options: {
          spawn: false,
          livereload: true,
        },
      },
    },

    // see: https://github.com/gruntjs/grunt-contrib-compass
    compass: {
      options: {
          sassDir: '<%= paths.sass %>',
          cssDir: '<%= paths.css %>',
          fontsDir: '<%= paths.fonts %>',
          imagesDir: '<%= paths.images %>',
          relativeAssets: false,
          assetCacheBuster: false,
          raw: 'Sass::Script::Number.precision = 10\n'
      },
      dist: {
        options: {
          environment: 'production'
        }
      },
      server: {
        options: {
          // debugInfo: true
        }
      }
    },

    // see: https://npmjs.org/package/grunt-bg-shell
    bgShell: {
      _defaults: {
        bg: true
      },
      runDjango: {
        cmd: 'python <%= paths.manageScript %> runserver'
      }
    },
    concat: {
      app: {
        src: [
              'bower_components/jquery/dist/jquery.js',
              'bower_components/angular/angular.js',
              'bower_components/angular-resource/angular-resource.js',
              'bower_components/angular-elastic/elastic.js',
              'bower_components/humanize/humanize.js',
              'bower_components/angularjs-humanize/src/angular-humanize.js',
              'bower_components/moment/moment.js',
              'bower_components/angular-moment/angular-moment.js',
              'bower_components/angular-nl2br/angular-nl2br.js',
              'bower_components/bootstrap/dist/js/bootstrap.js',
              'bower_components/bootbox.js/bootbox.js',


             ],
        dest: 'ekratia/static/dist/components.js'
      }
    },
    uglify: {
      app: {
        files: {'ekratia/static/dist/components.min.js': ['ekratia/static/dist/components.js']}
      }
    }
  });

  grunt.registerTask('serve', [
    'bgShell:runDjango',
    'watch'
  ]);

  grunt.registerTask('build', [
    'compass:dist'
  ]);

  grunt.registerTask('default', [
    'build'
  ]);

  grunt.registerTask('jsmin', [
    'concat:app'
    // 'uglify:app'
  ]);
};
