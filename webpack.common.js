const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const {CleanWebpackPlugin} = require('clean-webpack-plugin');

module.exports = {
    context: __dirname,
    entry: {
        gardenUpdate: './assets/gardenUpdate.js',
        gardenList: './assets/gardenList.js',
        gardenDetail: './assets/gardenDetail.js',
        wateringStationDetail: './assets/wateringStationDetail.js',
        wateringStationUpdate: './assets/wateringStationUpdate.js',
        vendor: './assets/vendor.js',
    },
    output: {
        filename: '[name]-[contenthash].js',
        path: path.resolve(__dirname, './static/javascript'),
    },
    plugins: [new BundleTracker({filename: './webpack-stats.json'}), new CleanWebpackPlugin()],
    module: {
        rules: [
            {
                test: /\.(js)$/,
                exclude: /node_modules/,
                loader: 'babel-loader',
                options: {presets: ['@babel/preset-env']},
            },
        ],
    },
};
