const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  mode: 'development',
  entry: './assets/js/index.js',
  output: {
        'path': path.resolve(__dirname, 'static'),
        filename: 'js/[name].[chunkhash].js',
    },
}