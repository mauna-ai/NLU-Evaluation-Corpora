const _ = require("lodash");

const pipeline = require("./pipeline");

const transform = (s, idx, all) => pipeline.reduce(
  (accumulator, current) =>
    async y => accumulator(
      await Promise.resolve(current(y, idx, all))
    ),
  async x => x
)(s, idx, all);

module.exports = {
  transform
};
