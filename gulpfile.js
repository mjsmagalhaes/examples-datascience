import gulp from 'gulp'

import { task } from 'gulp-execa'

export const build_package = task('python -m build')
build_package.displayName = 'build:package'

export const build_dsapps_backend = task('docker build --tag dslib:requirements --target requirements .')
build_dsapps_backend.displayName = 'build:backend'

export const build_dsapps_frontend = task('docker build --tag dslib:frontend --target frontend .')
build_dsapps_frontend.displayName = 'build:frontend'

// export const build_dsapps = gulp.series(build_dsapps_backend, build_dsapps_frontend)
// build_dsapps.displayName = 'build:dsapps'

export const build_dslib = task('docker build --tag dslib .')
build_dslib.displayName = 'build:app'

export const build_templates = task('npm run parcel:build')
build_templates.displayName = 'build:templates'

export const build_docs = task('mkdocs build')
build_docs.displayName = 'build:docs'

export const serve_docs = task('mkdocs serve')
serve_docs.displayName = 'serve:docs'

// export const run_dev_server = task('npm run parcel:dev:server')
// run_dev_server.displayName = 'run:dev:server'

// export const run_dev_gui = task('npm run electron:dev')
// run_dev_gui.displayName = 'run:dev:gui'

// export const run_dev = gulp.parallel(run_dev_server, run_dev_gui)
// run_dev.displayName = 'run:dev'

export const run_template = task('npm run parcel:watch')
run_template.displayName = 'run:template'

// export const run_app = task('heroku local -f Procfile.windows')
export const run_server = task('dsapps run')
run_server.displayName = 'run:server'

export const run_gui = task('npm run gui')
run_gui.displayName = 'run:gui'

// export const run = gulp.parallel(run_server, run_gui)

export const publish = task('git push heroku main')

export const shutdown = task('wsl --shutdown')

// 'heroku stack:set container'
// 'npx parcel serve --public-url /wordcloud/assets'

// 'docker run -it --name backend dslib:backend'
// 'docker run -it --name frontend dslib:frontend'

// 'docker commit backend dslib:backend'
// 'docker commit frontend dslib:frontend'