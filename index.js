// index.js

const { transform } = require("./utils");

const datasets = {
  ChatbotCorpus: require("./original/ChatbotCorpus.json"),
  AskUbuntuCorpus: require("./original/AskUbuntuCorpus.json"),
  WebApplicationCorpus: require("./original/WebApplicationCorpus.json"),
};

(async () => {
  for (let name of Object.keys(datasets)) {
    const dataset = datasets[name];
    const result = await Promise.all(
      dataset.sentences.map(transform)
    );

    const newDataset = {
      ...dataset,
      sentences: result
    };

    await fs.writeFile(`${name}.json`, JSON.stringify(newDataset, null 4));
  }
})()

  .then(console.log.bind("Success"), console.error.bind("Failed"));
