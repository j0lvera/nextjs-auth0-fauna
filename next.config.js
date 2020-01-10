const withCSS = require("@zeit/next-css");

module.exports = withCSS({
  env: {
    APP_URL: process.env.APP_URL,
    SECRET: process.env.SECRET
  },
  cssModules: true,
  target: "serverless",
  webpack: config => {
    // Fixes npm packages that depend on `fs` module
    config.node = {
      fs: "empty"
    };

    config.module.rules.push({
      test: /\.svg$/,
      use: [
        {
          loader: "@svgr/webpack"
        }
      ]
    });

    return config;
  }
});
