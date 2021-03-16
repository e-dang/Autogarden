const path = require('path');

module.exports = {
    entry: {
        gardenUpdate: './assets/gardenUpdate.js',
        gardenList: './assets/gardenList.js',
        gardenDetail: './assets/gardenDetail.js',
        wateringStationDetail: './assets/wateringStationDetail.js',
        wateringStationUpdate: './assets/wateringStationUpdate.js',
    },
    output: {
        filename: '[name].js',
        path: path.resolve(__dirname, './static/javascript'),
    },
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
