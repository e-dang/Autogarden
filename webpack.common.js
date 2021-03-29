const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const {CleanWebpackPlugin} = require('clean-webpack-plugin');

module.exports = {
    context: __dirname,
    entry: {
        gardenUpdate: './assets/js/gardenUpdate.js',
        gardenList: './assets/js/gardenList.js',
        gardenDetail: './assets/js/gardenDetail.js',
        wateringStationDetail: './assets/js/wateringStationDetail.js',
        wateringStationUpdate: './assets/js/wateringStationUpdate.js',
        vendor: './assets/js/vendor.js',
    },
    output: {
        filename: '[name]-[contenthash].js',
        path: path.resolve(__dirname, './assets/bundles'),
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
