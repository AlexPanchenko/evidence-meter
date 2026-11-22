// Keep the Chromium that mermaid-cli renders with inside node_modules: nothing installs globally.
const { join } = require('path')

module.exports = { cacheDirectory: join(__dirname, 'node_modules', '.cache', 'puppeteer') }
