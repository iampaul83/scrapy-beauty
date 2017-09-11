const pug = require('pug')
const fs = require('fs')
const posts = require('./beauty2.json')

const html = pug.renderFile('index.pug', { posts })
fs.writeFileSync('index.html', html, 'utf8')
