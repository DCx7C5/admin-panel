const path = require("path");
const BundleTracker = require("webpack-bundle-tracker");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
  context: __dirname,
  entry: {
    base: "./assets/js/index",
    login: "./assets/js/login"
  },
  output: {
    path: path.resolve(__dirname, "assets/webpack_bundles/"),
    filename: "[name]-[contenthash].js",
    clean: true,
  },
  devtool: "source-map",
  plugins: [
    new BundleTracker({ path: __dirname, filename: "webpack-stats.json" }),
    new MiniCssExtractPlugin({
      filename: "[name]-[contenthash].css",
    }),
  ],

  module: {
    rules: [
      // we pass the output from babel loader to react-hot loader
      {
        test: /\.(jsx|js)?$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
      {
        test: /\.css$/,
        use: [MiniCssExtractPlugin.loader, "css-loader"],
      },
    ],
  },

  resolve: {
    extensions: [".js", ".jsx"],
  },
};