const _ = require("lodash");

const corpus = {
  ChatbotCorpus: require("../original/ChatbotCorpus.json"),
  AskUbuntuCorpus: require("../original/AskUbuntuCorpus.json"),
  WebApplicationsCorpus: require("../original/WebApplicationsCorpus.json")
};

const getEntityClasses = corpus =>
  _(corpus.sentences)
    .map("entities")
    .map(ents => _.map(ents, "entity"))
    .flatten()
    .uniq()
    .value();

const entityClasses = {
  ChatbotCorpus: getEntityClasses(corpus.ChatbotCorpus),
  AskUbuntuCorpus: getEntityClasses(corpus.AskUbuntuCorpus),
  WebApplicationsCorpus: getEntityClasses(corpus.WebApplicationsCorpus)
};

const entityClassToHolmesMapping = {
  StationDest: "ENTITYFAC",
  Vehicle: "ENTITYPRODUCT",
  Criterion: "ENTITYNOUN",
  StationStart: "ENTITYFAC",
  Line: "ENTITYFAC",
  TimeStartTime: "ENTITYTIME",
  TimeEndTime: "ENTITYTIME",
  SoftwareName: "ENTITYPRODUCT",
  UbuntuVersion: "ENTITYNOUN",
  Printer: "ENTITYPRODUCT",
  WebService: "ENTITYNOUN",
  Browser: "ENTITYPRODUCT",
  OperatingSystem: "ENTITYPRODUCT"
};

module.exports = {
  corpus,
  entityClasses,
  entityClassToHolmesMapping
};
