const $ = require("got");
const _ = require("lodash");

const constants = require("./utils/constants");
const utils = require("./utils");

const context = {
  ...constants,
  $,
  _,
  utils
};

module.exports = {
  context,
  enableAwait: true
};
