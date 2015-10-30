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
      manageScript: 'manage.py',
      
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
      sass: {
        files: ['<%= paths.sass %>/**/*.{scss,sass}'],
        tasks: ['sass:dev'],
        options: {
          atBegin: true
        }
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

    // see: https://github.com/sindresorhus/grunt-sass
    sass: {
      dev: {
          options: {
              outputStyle: 'nested',
              sourceMap: false,
              precision: 10
          },
          files: {
              '<%= paths.css %>/project.css': '<%= paths.sass %>/project.scss'
          },
      },
      dist: {
          options: {
              outputStyle: 'compressed',
              sourceMap: false,
              precision: 10
          },
          files: {
              '<%= paths.css %>/project.css': '<%= paths.sass %>/project.scss'
          },
      }
    },
    
    //see https://github.com/nDmitry/grunt-postcss
    postcss: {
      options: {
        map: true, // inline sourcemaps

        processors: [
          require('pixrem')(), // add fallbacks for rem units
          require('autoprefixer-core')({browsers: [
            'Android 2.3',
            'Android >= 4',
            'Chrome >= 20',
            'Firefox >= 24',
            'Explorer >= 8',
            'iOS >= 6',
            'Opera >= 12',
            'Safari >= 6'
          ]}), // add vendor prefixes
          require('cssnano')() // minify the result
        ]
      },
      dist: {
        src: '<%= paths.css %>/*.css'
      }
    },

    // see: https://npmjs.org/package/grunt-bg-shell
    bgShell: {
      _defaults: {
        bg: true
      },
      runDjango: {
        cmd: 'python <%= paths.manageScript %> runserver 0.0.0.0:9000'
      },
      
    },
    concat: {
      app: {
        src: [
              'bower_components/jquery/dist/jquery.js',
              'bower_components/angular/angular.js',
              'bower_components/angular-resource/angular-resource.js',
              'bower_components/angular-sanitize/angular-sanitize.js',
              'bower_components/angular-elastic/elastic.js',
              'bower_components/humanize/humanize.js',
              'bower_components/angularjs-humanize/src/angular-humanize.js',
              'bower_components/moment/moment.js',
              'bower_components/angular-moment/angular-moment.js',
              'bower_components/angular-nl2br/angular-nl2br.js',
              'bower_components/bootstrap/dist/js/bootstrap.js',
              'bower_components/bootbox.js/bootbox.js',
              'bower_components/ngBootbox/dist/ngBootbox.js',
              'bower_components/pluralize/pluralize.js',
              'bower_components/spin.js/spin.js',
              'bower_components/angular-spinner/angular-spinner.js',
              'bower_components/angular-loading-spinner/angular-loading-spinner.js',
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
    'sass:dist',
    'postcss'
  ]);

  grunt.registerTask('default', [
    'build'
  ]);

  grunt.registerTask('jsmin', [
    'concat:app',
    'uglify:app'
  ]);

};
