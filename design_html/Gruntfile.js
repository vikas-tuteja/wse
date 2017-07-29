module.exports = function (grunt) {
  var mainfolder = 'app/'
  var scsspath = mainfolder + 'scss/'
  var _libscss = scsspath + 'lib'
  var _innercss = scsspath + '*.css'
  var _innerscss = scsspath + '*.scss'
  var _jspath = 'app/js'
  var _imagepath = mainfolder + 'images'
  var _htmlpath = 'app/html'

  grunt.initConfig({
    watch: {
      grunt: {
        files: ['Gruntfile.js']
      },
      css: {
        files: [_innercss],
        tasks: ['copy:css']
      },
      images: {
        files: [_imagepath, _imagepath + '/**/*'],
        tasks: ['copy:img']
      },
      js: {
        files: [_jspath + "/*"],
        tasks: ['copy:js']
      },
      html: {
        files: [_htmlpath + '/*.njk', _htmlpath + '/**/*.njk', _htmlpath + '/**/*html', _htmlpath + '/*.html'],
        tasks: ['nunjucks', 'htmlhintplus'],
        options: {
          spawn: false,
          livereload: true
        }
      },
      sass: {
        files: [_innerscss, scsspath + '**/*.scss', scsspath + "*"],
        tasks: ['sass', 'postcss', 'notify:sass'],
        options: {
          spawn: false
        }

      }
    },

    copy: {
      css: {
        expand: true,
        cwd: scsspath,
        src: ['*.css'],
        dest: 'build/css',
        filter: 'isFile'
      },
      js: {
        expand: true,
        cwd: _jspath,
        src: ['*'],
        dest: 'build/js',
        filter: 'isFile'
      },
      img: {
        expand: true,
        cwd: _imagepath,
        src: ['*'],
        dest: 'build/images',
        filter: 'isFile'
      }
    },
    nunjucks: {
      options: {
        data: grunt.file.readJSON('data.json')
      },
      render: {
        files: [{
          expand: true,
          cwd: _htmlpath,
          src: ['**/*.html', '*.html'],
          dest: 'build/',
          ext: '.html'
        }]
      }
    },
    sass: {
      dist: {
        options: {
          style: 'expanded',
          loadPath: _libscss
        },
        files: [{
          expand: true,
          cwd: scsspath,
          src: ['**/*.scss'],
          dest: 'build/css',
          ext: '.css'
        }]
      }
    },

    notify: {
      sass: {
        options: {
          title: 'CSS Files built ',
          message: 'SCSS compile task complete'
        }
      },
      server: {
        options: {
          message: 'Server is ready!'
        }
      }
    },

    htmlhintplus: {
      build: {
        src: 'html/index.html',
        options: {
          rules: {
            'attr-lowercase': false
          }
        }
      }
    },

    imagemin: {
      dynamic: {
        options: {
          optimizationLevel: 7
        },
        files: [{
          expand: true,
          cwd: _imagepath,
          src: ['{,*/}*.{png,jpg,gif,svg}'],
          dest: 'build/images/'
        }]
      }
    },

    postcss: {
      options: {
        safe: true,
        processors: [
          require('autoprefixer')({
            browsers: [
              'last 60 versions',
              'ie 9'
            ]
          })
        ],
        map: true
      },

      // Prefix all files
      multiple_files: {
        flatten: true,
        src: 'build/css/*.css'
      }
    },

    browserSync: {
      bsFiles: {
        src: [
          'build/css/*.css',
          'build/js/*.js',
          'build/*.html'
        ]
      },
      options: {
        watchTask: true,
        server: 'build/'
      }
    }
  })

  // Load the plugins to run your tasks
  require('load-grunt-tasks')(grunt, {
    scope: 'devDependencies'
  })

  grunt.registerTask('default', 'html templates', ['copy', 'nunjucks', 'browserSync', 'sass', 'postcss', 'notify:server', 'watch'])
}
