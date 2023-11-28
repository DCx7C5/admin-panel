const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  mode: 'development',
  context: __dirname,
  entry: './assets/js/index.js',
  output: {
    path: path.resolve('./js/webpack_bundles/'),
    filename: "[name]-[fullhash].js"
  },
  plugins: [
    new BundleTracker({path: __dirname, filename: 'webpack-stats.json'})
  ],
}