const got = require("got");

const paraphrase = async (sentence, endpoint="http://localhost:5000") =>
  (await got(
    `${endpoint}/paraphrase`,
    { searchParams: { sentence }, responseType: 'json' }
  )).body.result;

module.exports = {
  paraphrase
};
